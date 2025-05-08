const toggleBtn = document.getElementById('themeToggle');
const appleLogo = document.getElementById('appleLogo');
const diwanLogo = document.querySelector('.logodiwan');

let darkMode = false;

toggleBtn.addEventListener('click', () => {
  darkMode = !darkMode;
  document.body.classList.toggle('dark-mode');
  toggleBtn.src = darkMode ? "/img/light_mode.png" : "/img/moon.png";
  toggleBtn.alt = darkMode ? "Mode jour" : "Mode nuit";
  
  if (diwanLogo) {
    diwanLogo.src = "/img/Diwanlogo-removebg.png";
  }
});

document.getElementById("loginBtn").addEventListener("click", function () {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  // Si les deux champs sont vides
  if (!email && !password) {
    alert("Veuillez remplir les champs précédents.");
    return;
  }

  // Vérification spécifique si un seul champ est vide
  if (!email) {
    alert("Veuillez insérer votre E-mail.");
    return;
  }

  if (!password) {
    alert("Veuillez insérer votre mot de passe.");
    return;
  }

  // Vérification de validité du contenu
  const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  const passwordValid = password.length >= 6;

  if (!emailValid) {
    alert("Veuillez entrer un email valide.");
    return;
  }

  if (!passwordValid) {
    alert("Le mot de passe doit contenir au moins 6 caractères.");
    return;
  }

  alert("Connexion réussie !");
});
