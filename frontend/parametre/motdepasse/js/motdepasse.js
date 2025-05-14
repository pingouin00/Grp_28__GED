document.getElementById('forgot-password-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Récupérer la valeur de l'email
    const email = document.getElementById('email').value;

    // Expression régulière pour valider le format de l'email
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    // Vérifier si l'email correspond au format
    if (!emailRegex.test(email)) {
        // Afficher un message d'erreur si l'email n'est pas valide
        document.getElementById('error-message').innerText = "Veuillez entrer un e-mail valide.";
    } else {
        // Si l'email est valide, vous pouvez ajouter ici la logique pour envoyer un e-mail de réinitialisation
        document.getElementById('error-message').innerText = ""; // Effacer le message d'erreur
        alert("Un lien pour réinitialiser votre mot de passe a été envoyé à " + email);
    }
});