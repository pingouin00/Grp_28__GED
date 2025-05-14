// Validation des champs
function valider() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const phone = document.getElementById("phone").value;
  const errorMessage = document.getElementById("error-message");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const phoneRegex = /^[0-9]{10,15}$/;

  if (!username.trim()) {
    errorMessage.innerText = "Veuillez entrer un nom.";
    return;
  }

  if (!emailRegex.test(email)) {
    errorMessage.innerText = "Adresse e-mail invalide.";
    return;
  }

  if (!phoneRegex.test(phone)) {
    errorMessage.innerText = "Numéro de téléphone invalide (10 à 15 chiffres).";
    return;
  }

  errorMessage.innerText = "";
  localStorage.setItem("nomUtilisateur", username);
  alert("Informations enregistrées avec succès !");
  document.getElementById("welcome-msg").innerText = `Salut ${username} !`;
}

// Affichage du nom sauvegardé
document.addEventListener("DOMContentLoaded", () => {
  const nomUtilisateur = localStorage.getItem("nomUtilisateur");
  if (nomUtilisateur) {
    document.getElementById("welcome-msg").innerText = `Salut ${nomUtilisateur} !`;
    document.getElementById("username").value = nomUtilisateur;
  }

  // Navigation
  document.getElementById("btn-home").addEventListener("click", () => {
    window.location.href = "../homepage/homepage.html";
  });

  document.getElementById("btn-user").addEventListener("click", () => {
    window.location.href = "../userpage/user.html";
  });

  document.getElementById("btn-history").addEventListener("click", () => {
    window.location.href = "../historique/historique.html";
  });

  document.getElementById("btn-settings").addEventListener("click", () => {
    window.location.href = "../parametre/parametre.html";
  });

  document.getElementById("btn-logout").addEventListener("click", () => {
    alert("Déconnexion non encore implémentée.");
  });
});