#  Gestion Documentaire avec Moteur de Recherche

Système de **Gestion Électronique de Documents (GED)** développé par le groupe 28. Ce projet vise à faciliter la gestion, la recherche intelligente et la sécurisation des documents dans une interface moderne et intuitive.

---

##  Fonctionnalités principales

###  Gestion des utilisateurs et sécurité
- Authentification sécurisée (connexion/déconnexion)
- Gestion des rôles et permissions
- Historique des connexions et actions
- Mise à jour du profil utilisateur
- Chiffrement des données confidentielles

###  Gestion des documents
- Téléversement multi-formats (PDF, DOCX, images…)
- Extraction automatique de métadonnées
- Classification avec tags et catégories
- Conversion OCR pour documents scannés
- Modification / suppression de documents

###  Recherche intelligente
- Moteur de recherche par mots-clés
- Suggestions automatiques en temps réel
- Recherche sémantique (similarité de contenu)
- Mise en surbrillance des résultats
- Filtres par auteur, date, catégorie

###  Interface utilisateur
- Tableau de bord des documents récents
- Prévisualisation de documents (PDF, images…)
- Navigation fluide avec pagination
- Interface moderne et responsive

###  Machine Learning & Analyse
- Classification automatique (TF-IDF + KNN)
- Détection de sujets (topic modeling)
- Retour utilisateur pour améliorer les résultats
- Statistiques d’usage et d’activité

---

##  Technologies utilisées

- **Frontend** : React.js (interface dynamique et responsive)
- **Backend** : Python (framework Django)
- **Base de données** : MongoDB (NoSQL, flexible et scalable)
- **Machine Learning** : Scikit-learn, NLTK, Pandas, TF-IDF
- **OCR** : Tesseract OCR (reconnaissance de texte dans les images)
- **Sécurité** : Authentification JWT (JSON Web Token)
- **Déploiement** : GitHub (gestion de version et collaboration)

---

##  User Stories

> Les 23 User Stories sont disponibles dans la section "Issues" du dépôt.  
> Elles couvrent la sécurité, la gestion documentaire, la recherche, l'expérience utilisateur et l'intelligence artificielle.

---

##  Objectifs pédagogiques

- Mettre en pratique l'ingénierie logicielle en groupe
- Appliquer des techniques de traitement de texte et NLP
- Intégrer un moteur de recherche avancé
- Implémenter un système GED intelligent et sécurisé

---

##  Équipe projet Grp_28__GED

-  **pingouin00** — Scrum Master / Responsable GitHub
-  **Shaimaedb** — Développeuse
-  **MarouaBenjelloun** — Développeuse
-  **Aassim-Zakariae** — Développeur

---

# Pour Cloner le projet
git clone https://github.com/pingouin00/Grp_28__GED.git
cd Grp_28__GED

# Installer les dépendances (exemple pour un backend Python)
pip install -r requirements.txt

# Lancer le serveur (exemple Flask)
python app.py

