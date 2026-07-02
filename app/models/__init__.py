from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))


class Localisation(db.Model):
    __tablename__ = 'localisations'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    quartier = db.Column(db.String(100))

    annonces = db.relationship('AnnonceDon', backref='localisation', lazy=True)
    structures = db.relationship('Structure', backref='localisation', lazy=True)
    missions = db.relationship('MissionVolontariat', backref='localisation', lazy=True)

    def __repr__(self):
        return f'{self.quartier}, {self.ville} ({self.region})'


class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(256), nullable=False)
    # 'donateur', 'benevole', 'admin'
    role = db.Column(db.String(20), default='donateur')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    annonces = db.relationship('AnnonceDon', backref='auteur', lazy=True)
    promesses = db.relationship('PromesseDon', backref='donateur', lazy=True)
    candidatures = db.relationship('Candidature', backref='benevole', lazy=True)

    def set_password(self, password):
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)

    def is_admin(self):
        return self.role == 'admin'


class AnnonceDon(db.Model):
    __tablename__ = 'annonces_dons'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisations.id'))
    # 'habits', 'alimentation', 'cosmetique'
    categorie = db.Column(db.String(50), nullable=False)
    # 'enfants', 'hommes', 'femmes' pour habits; 'riz','huile',... pour alim; etc.
    sous_categorie = db.Column(db.String(50))
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    # 'en_attente', 'approuve', 'rejete', 'termine'
    statut = db.Column(db.String(20), default='en_attente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Structure(db.Model):
    __tablename__ = 'structures'
    id = db.Column(db.Integer, primary_key=True)
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisations.id'))
    nom = db.Column(db.String(200), nullable=False)
    # 'daara', 'ecole', 'hopital', 'mosquee', 'ong'
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    contact = db.Column(db.String(100))
    numero_orange_money = db.Column(db.String(20))
    numero_wave = db.Column(db.String(20))
    verifie = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255))

    promesses = db.relationship('PromesseDon', backref='structure', lazy=True)
    missions = db.relationship('MissionVolontariat', backref='structure', lazy=True)


class PromesseDon(db.Model):
    __tablename__ = 'promesses_dons'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    structure_id = db.Column(db.Integer, db.ForeignKey('structures.id'), nullable=False)
    montant = db.Column(db.Numeric(10, 2), nullable=False)
    # 'orange_money', 'wave'
    operateur = db.Column(db.String(30), nullable=False)
    # 'promesse', 'effectue'
    statut = db.Column(db.String(20), default='promesse')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MissionVolontariat(db.Model):
    __tablename__ = 'missions_volontariat'
    id = db.Column(db.Integer, primary_key=True)
    structure_id = db.Column(db.Integer, db.ForeignKey('structures.id'), nullable=False)
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisations.id'))
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    competences_requises = db.Column(db.String(300))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    places_disponibles = db.Column(db.Integer, default=5)
    active = db.Column(db.Boolean, default=True)

    candidatures = db.relationship('Candidature', backref='mission', lazy=True)


class Candidature(db.Model):
    __tablename__ = 'candidatures'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions_volontariat.id'), nullable=False)
    message = db.Column(db.Text)
    # 'en_attente', 'accepte', 'refuse'
    statut = db.Column(db.String(20), default='en_attente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
