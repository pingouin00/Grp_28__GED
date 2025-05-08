// Exemple : afficher un message statique
document.getElementById("resultat").innerText = "Traitement en cours...";

// Plus tard tu pourras faire quelque chose comme ça :
/*
fetch("/api/resultats")
  .then(response => response.json())
  .then(data => {
    document.getElementById("resultat").innerText = data.message;
  });
*/// Exemple : afficher un message statique
document.getElementById("resultat").innerText = "Traitement en cours...";

// Plus tard tu pourras faire quelque chose comme ça :
/*
fetch("/api/resultats")
  .then(response => response.json())
  .then(data => {
    document.getElementById("resultat").innerText = data.message;
  });
*/