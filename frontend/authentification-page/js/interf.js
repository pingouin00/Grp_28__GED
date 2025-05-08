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
