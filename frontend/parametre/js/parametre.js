document.addEventListener('DOMContentLoaded', function() {

    const btnNotifications = document.getElementById('btn-notifications');
    const notificationStatus = document.getElementById('notification-status');
    const confirmationMsg = document.getElementById('delete-msg');
    const btnDeleteAccount = document.getElementById('btn-delete-account');
    const btnConfirmDelete = document.getElementById('confirm-delete');

    // Activation / Désactivation des notifications
    btnNotifications.addEventListener('click', function() {
        if (btnNotifications.classList.contains('inactive')) {
            // Activer les notifications
            btnNotifications.classList.remove('inactive');
            btnNotifications.classList.add('active');
            notificationStatus.textContent = '✅ Notifications activées';
        } else {
            // Désactiver les notifications
            btnNotifications.classList.remove('active');
            btnNotifications.classList.add('inactive');
            notificationStatus.textContent = '❌ Notifications désactivées';
        }
    });

    // Affichage de la confirmation pour supprimer le compte
    btnDeleteAccount.addEventListener('click', function() {
        confirmationMsg.style.display = 'block';
    });

    // Confirmation de suppression du compte
    btnConfirmDelete.addEventListener('click', function() {
        alert('Votre compte a été supprimé !');
        confirmationMsg.style.display = 'none';
    });

    // Redirection vers la page "Mot de passe oublié"
    document.getElementById('btn-forgot-password').addEventListener('click', function () {
        window.location.href = "./motdepasse/motdepasse.html";
    });

    // Redirections pour la barre latérale
    document.getElementById('btn-home').addEventListener('click', function() {
        window.location.href = "../homepage/homepage.html"; // Redirection vers la page d'accueil
    });

    document.getElementById('btn-user').addEventListener('click', function() {
        window.location.href = "../userpage/user.html"; // Redirection vers la page utilisateur
    });

    document.getElementById('btn-history').addEventListener('click', function() {
        window.location.href = "../historique/historique.html"; // Redirection vers la page historique
    });

    document.getElementById('btn-settings').addEventListener('click', function() {
        window.location.href = "parametre.html"; // Redirection vers la page paramètres
    });

    document.getElementById('btn-logout').addEventListener('click', function() {
        window.location.href = "login.html"; // Redirection vers la page de connexion (exemple)
    });
});