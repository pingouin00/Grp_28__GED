document.addEventListener("DOMContentLoaded", () => {
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