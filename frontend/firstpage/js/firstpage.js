// Attendre que la page soit complètement chargée
window.addEventListener('DOMContentLoaded', () => {
    const btnApropos = document.getElementById('btn-apropos');
    const btnCommencer = document.getElementById('btn-commencer');
  
    btnApropos.addEventListener('click', () => {
      window.location.href = '../about-page/Apropos.html';
    });
  
    btnCommencer.addEventListener('click', () => {
      window.location.href = '../authentification-page/interf.html';
    });
  });
  