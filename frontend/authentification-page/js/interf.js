const toggleBtn = document.getElementById('themeToggle');

let darkMode = false;

toggleBtn.addEventListener('click', () => {
  darkMode = !darkMode;
  document.body.classList.toggle('dark-mode');
  toggleBtn.src = darkMode ? "./img/light_mode.png" : "./img/moon.png";
  toggleBtn.alt = darkMode ? "Mode jour" : "Mode nuit";
  
});

document.getElementById('signup').addEventListener('click', function() {
  window.location.href = '../inscription-page/inscription.html';
});

document.getElementById('login').addEventListener('click', function() {
  window.location.href = '../connexion-page/connexion.html';
});
