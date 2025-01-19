// Lomakkeen validointia varten (valinnat pakollisiksi)
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        const questions = document.querySelectorAll("input[type=radio]");
        let allAnswered = true;

        // Tarkista, että jokaisesta kysymyksestä on valittu vastaus
        const questionGroups = [...new Set([...questions].map(input => input.name))];
        questionGroups.forEach(group => {
            if (!document.querySelector(`input[name="${group}"]:checked`)) {
                allAnswered = false;
            }
        });

        if (!allAnswered) {
            event.preventDefault();
            alert("Please answer all questions before submitting.");
        }
    });
});
