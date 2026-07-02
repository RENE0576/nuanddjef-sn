# 🇸🇳 BarakaSN — Dons & Volontariat au Sénégal

Projet étudiant — Site web dynamique centralisant les dons (habits, produits, argent) et le volontariat au Sénégal.

---

## ⚡ Installation rapide (5 étapes)

### Prérequis
- Python 3.10+
- PostgreSQL installé et démarré
- VS Code avec terminal intégré (`Ctrl + `` `)

### 1. Créer l'environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer l'environnement
```bash
cp .env.example .env
# Éditez .env et changez DATABASE_URL avec votre config PostgreSQL
```

Contenu du `.env` :
```
SECRET_KEY=une-cle-secrete-longue-et-aleatoire
DATABASE_URL=postgresql://postgres:motdepasse@localhost/senegal_dons
```

### 4. Créer la base de données et migrer
```bash
# Dans psql ou pgAdmin : CREATE DATABASE senegal_dons;
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

### 5. Peupler + lancer
```bash
python seed.py      # données de démonstration
python run.py       # démarrer le serveur
```
➡️ Ouvrir **http://localhost:5000**

---

## 👤 Comptes de test

| Rôle     | Email               | Mot de passe |
|----------|---------------------|--------------|
| Admin    | admin@barakasn.sn   | admin1234    |
| Donateur | fatou@test.sn       | test1234     |
| Bénévole | moussa@test.sn      | test1234     |

---

## 📁 Structure complète du projet

```
senegal_dons/
├── run.py                        # Point d'entrée Flask
├── config.py                     # Configuration (DB, uploads…)
├── seed.py                       # Données de démonstration
├── requirements.txt
├── .env.example
│
├── app/
│   ├── __init__.py               # Factory Flask + erreurs 404/500
│   ├── utils.py                  # Helper upload d'images
│   │
│   ├── models/
│   │   └── __init__.py           # 6 modèles SQLAlchemy :
│   │                             #   Utilisateur, Localisation,
│   │                             #   AnnonceDon, Structure,
│   │                             #   PromesseDon, MissionVolontariat,
│   │                             #   Candidature
│   ├── routes/
│   │   ├── main.py               # Accueil
│   │   ├── auth.py               # Inscription, connexion, mon espace
│   │   ├── dons.py               # Habits, produits, argent, annonces
│   │   ├── volontariat.py        # Missions, candidatures
│   │   └── admin.py              # Modération complète
│   │
│   ├── templates/
│   │   ├── base.html             # Layout mobile-first complet
│   │   ├── index.html            # Page d'accueil
│   │   ├── 404.html / 500.html   # Pages d'erreur
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── inscription.html
│   │   │   └── mon_espace.html   # Dashboard utilisateur
│   │   ├── dons/
│   │   │   ├── habits.html       # Liste avec filtres
│   │   │   ├── produits.html
│   │   │   ├── argent.html       # Modal Orange Money / Wave
│   │   │   ├── creer_annonce.html # Upload photo + JS dynamique
│   │   │   └── detail_annonce.html
│   │   ├── volontariat/
│   │   │   ├── index.html        # Filtres Région/Ville/Quartier
│   │   │   └── detail.html       # Candidature intégrée
│   │   └── admin/
│   │       ├── dashboard.html    # Vue d'ensemble avec alertes
│   │       ├── annonces.html     # Modération approuver/rejeter
│   │       ├── candidatures.html # Accepter/refuser bénévoles
│   │       ├── structures.html   # Liste structures
│   │       ├── ajouter_structure.html
│   │       ├── missions.html     # Activer/désactiver missions
│   │       ├── ajouter_mission.html
│   │       └── localisations.html # Gérer Région/Ville/Quartier
│   │
│   └── static/
│       └── img/uploads/          # Photos uploadées (auto-créé)
```

---

## 📱 Fonctionnalités mobiles

| Fonctionnalité | Description |
|---|---|
| Menu hamburger | Panneau latéral animé avec overlay |
| Bottom navigation | Barre fixe en bas (style app native) |
| Filtres scrollables | Pills horizontales sans coupure |
| Cards scroll | Annonces en carrousel horizontal sur mobile |
| Modal bottom sheet | Fenêtre de don qui monte du bas |
| Touch targets 44px | Tous les boutons facilement cliquables |
| Font-size 16px | Inputs sans zoom automatique sur iOS |
| Safe area iPhone | Compatible avec les encoches |
| Upload drag & drop | Photo glissable ou cliquable |

---

## 🔗 Toutes les routes disponibles

```
GET  /                            → Accueil
GET  /dons/habits                 → Liste habits (filtre sous-catégorie)
GET  /dons/produits               → Liste produits (filtre catégorie)
GET  /dons/argent                 → Structures + modal don
POST /dons/argent/<id>/promettre  → Enregistrer promesse de don
GET  /dons/annonce/<id>           → Détail annonce
GET  /dons/annonce/creer          → Formulaire création (auth requis)
POST /dons/annonce/<id>/supprimer → Supprimer annonce (auth requis)
POST /dons/annonce/<id>/terminer  → Marquer comme terminée

GET  /volontariat/                → Liste missions (filtres geo)
GET  /volontariat/<id>            → Détail + candidature
POST /volontariat/<id>/postuler   → Postuler (auth requis)

GET  /auth/inscription            → Formulaire inscription
GET  /auth/connexion              → Formulaire connexion
GET  /auth/deconnexion            → Déconnexion
GET  /auth/mon-espace             → Dashboard utilisateur (auth requis)

GET  /admin/                      → Dashboard admin (admin requis)
GET  /admin/annonces              → Modération annonces
POST /admin/annonces/<id>/approuver
POST /admin/annonces/<id>/rejeter
GET  /admin/structures            → Liste structures
GET  /admin/structures/ajouter
POST /admin/structures/<id>/supprimer
GET  /admin/missions              → Liste missions
GET  /admin/missions/ajouter
POST /admin/missions/<id>/toggle
POST /admin/missions/<id>/supprimer
GET  /admin/candidatures          → Liste candidatures
POST /admin/candidatures/<id>/accepter
POST /admin/candidatures/<id>/refuser
GET  /admin/localisations         → Gestion localités
POST /admin/localisations/ajouter
POST /admin/localisations/<id>/supprimer
```

---

## 🚀 Déploiement sur Render.com (gratuit)

1. Créer un compte sur [render.com](https://render.com)
2. **New → Web Service** → connecter votre repo GitHub
3. Paramètres :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn run:app`
4. **New → PostgreSQL** → copier l'URL dans les variables d'environnement
5. Ajouter les variables : `SECRET_KEY`, `DATABASE_URL`
6. Ajouter `gunicorn` dans `requirements.txt`

---

## 🛠 Prochaines améliorations possibles

- 🔔 Notifications email (Flask-Mail) quand une annonce est approuvée
- 🔍 Recherche textuelle sur les annonces
- 📄 Pagination sur les listes
- 🗺 Carte interactive des structures (Leaflet.js + OpenStreetMap)
- 💬 Messagerie interne entre donateur et receveur
- 📊 Page statistiques publique (dons collectés, bénévoles actifs)
