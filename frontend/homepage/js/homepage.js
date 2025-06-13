document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const explorerBtn = document.getElementById("explorerBtn");
    const errorMessage = document.getElementById("errorMessage");
  
    explorerBtn.addEventListener("click", function () {
      const value = searchInput.value.trim();
  
      if (value === "") {
        // Affiche le message d'erreur si l'input est vide
        errorMessage.textContent = "Veuillez remplir le champ de recherche.";
        errorMessage.style.display = "block";
      } else {
        // Redirige vers une autre page si l'input est non vide
        window.location.href = `../resultatdurecherche/resultat.html?query=${encodeURIComponent(value)}`;
      }
    });
   // Redirection vers la page d'accueil lorsque l'icône "Home" est cliquée
   document.getElementById("btn-home").addEventListener("click", function () {
    window.location.href = "../homepage/homepage.html";
  });

    // Effacer le message d'erreur si l'utilisateur commence à taper
    searchInput.addEventListener("input", function () {
      errorMessage.style.display = "none";
    });
  });
