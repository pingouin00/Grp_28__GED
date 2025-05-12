function valider() {
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const errorMessage = document.getElementById("error-message");
  
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[0-9]{10,15}$/;
  
    if (!emailRegex.test(email)) {
      errorMessage.innerText = "Adresse e-mail invalide.";
      errorMessage.style.display = "block";
      return;
    }
  
    if (!phoneRegex.test(phone)) {
      errorMessage.innerText = "Numéro de téléphone invalide (10 à 15 chiffres).";
      errorMessage.style.display = "block";
      return;
    }
  
    errorMessage.innerText = "";
    alert("Informations enregistrées avec succès !");
  }
  
  // Navigation
  document.getElementById("btn-home").addEventListener("click", () => {
    window.location.href = "homepage.html";
  });
  
  document.getElementById("btn-history").addEventListener("click", () => {
    window.location.href = "historique.html";
  });
  
  document.getElementById("btn-settings").addEventListener("click", () => {
    window.location.href = "parametre.html";
  });