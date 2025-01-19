from flask import Flask, render_template, request, session
import json
import random
import os

# Flask-sovellus
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Lisää salainen avain sessioiden hallintaan

# Lisää enumerate Jinja2:n käyttöön
app.jinja_env.globals.update(enumerate=enumerate)

def load_questions(filename):
    """
    Lataa kysymykset JSON-tiedostosta.
    """
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def quiz():
    """
    Kysymyssivu, jossa käyttäjä vastaa monivalintakysymyksiin.
    """
    if request.method == 'POST':
        user_answers = request.form  # Käyttäjän vastaukset
        score = 0

        # Lataa kysymykset sessiosta
        selected_questions = session.get('selected_questions', [])
        if not selected_questions:
            return "Error: No questions found in session.", 400

        # Muunna käyttäjän vastaukset sanakirjaksi
        user_answers_dict = {
            f"q{index + 1}": user_answers.get(f"q{index + 1}", "")
            for index, _ in enumerate(selected_questions)
        }

        # Tarkista käyttäjän vastaukset ja laske pisteet
        for index, question in enumerate(selected_questions, 1):
            user_answer = user_answers_dict.get(f"q{index}", "").strip().lower()
            correct_answer = question["answer"].strip().lower()
            if user_answer == correct_answer:
                score += 1

        # Näytä Tarot-kortti vain, jos kaikki vastaukset ovat oikein
        chosen_card = None
        if score == len(selected_questions):
            tarot_cards = load_questions('kortit.json')
            if tarot_cards:
                chosen_card = random.choice(tarot_cards)

        # Välitä tulokset, kysymykset ja vastaukset result.html-tiedostoon
        return render_template(
            'result.html',
            score=score,
            total=len(selected_questions),
            card=chosen_card,
            questions=selected_questions,
            user_answers=user_answers_dict
        )

    # GET-pyyntö: Valitse kysymykset ja tallenna ne sessioon
    questions = load_questions('kysymykset.json')
    num_questions = 3
    selected_questions = random.sample(questions, min(num_questions, len(questions)))
    session['selected_questions'] = selected_questions  # Tallenna sessioon

    return render_template('quiz.html', questions=selected_questions)

if __name__ == '__main__':
    app.run()
