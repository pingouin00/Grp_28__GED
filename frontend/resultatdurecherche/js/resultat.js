document.addEventListener("DOMContentLoaded", function () {
    // Fonction pour récupérer les paramètres de l'URL
    function getQueryParam(param) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
    }
  
    // Récupérer la valeur du paramètre "query" de l'URL
    const query = getQueryParam('query');
  
    // Afficher la valeur de la recherche dans la page
    const resultElement = document.getElementById("resultat");
  
    if (query) {
      // Affiche la recherche sur la page
      resultElement.innerText = `Résultats pour : ${query}`;
    } else {
      resultElement.innerText = "Aucun résultat trouvé.";
    }
  
    // Redirection vers la page d'accueil lorsque l'icône "Home" est cliquée
    document.getElementById("btn-home").addEventListener("click", function () {
      window.location.href = "../homepage/homepage.html";
    });
  });