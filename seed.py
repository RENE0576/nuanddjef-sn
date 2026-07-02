"""
Script de données de démonstration.
Lance avec : python seed.py
"""
from run import app
from app import db
from app.models import Utilisateur, Localisation, Structure, AnnonceDon, MissionVolontariat
from datetime import date

with app.app_context():
    db.create_all()

    # ── Localisations ─────────────────────────────────────────────────────
    locs = [
        Localisation(region='Dakar',    ville='Dakar',  quartier='Médina'),
        Localisation(region='Dakar',    ville='Dakar',  quartier='Pikine'),
        Localisation(region='Thiès',    ville='Mbour',  quartier='Centre'),
        Localisation(region='Thiès',    ville='Thiès',  quartier='Randoulène'),
        Localisation(region='Saint-Louis', ville='Saint-Louis', quartier='Nord'),
        Localisation(region='Ziguinchor', ville='Ziguinchor', quartier='Boucotte'),
    ]
    db.session.add_all(locs)
    db.session.flush()

    # ── Admin user ────────────────────────────────────────────────────────
    admin = Utilisateur(nom='Admin BarakaSN', email='admin@barakasn.sn', role='admin')
    admin.set_password('admin1234')
    user1 = Utilisateur(nom='Fatou Ndiaye', email='fatou@test.sn', role='donateur')
    user1.set_password('test1234')
    user2 = Utilisateur(nom='Moussa Diop', email='moussa@test.sn', role='benevole')
    user2.set_password('test1234')
    db.session.add_all([admin, user1, user2])
    db.session.flush()

    # ── Structures ────────────────────────────────────────────────────────
    structures = [
        Structure(nom='Daara Serigne Touba', type='daara', description='École coranique accueillant 200 talibés.',
                  contact='+221 77 000 0001', numero_orange_money='771000001', numero_wave='771000001',
                  localisation_id=locs[0].id, verifie=True),
        Structure(nom='Hôpital Le Dantec', type='hopital', description='Hôpital public de Dakar.',
                  contact='+221 33 849 0000', numero_orange_money='338490000',
                  localisation_id=locs[0].id, verifie=True),
        Structure(nom='ONG JED', type='ong', description='Journalistes pour les Droits de l\'Homme et la Démocratie.',
                  contact='+221 77 111 2233', numero_wave='771112233',
                  localisation_id=locs[1].id, verifie=True),
        Structure(nom='CODEVS', type='ong', description='Conseil pour le Développement du Volontariat au Sénégal.',
                  contact='+221 77 444 5566', numero_orange_money='774445566', numero_wave='774445566',
                  localisation_id=locs[0].id, verifie=True),
        Structure(nom='Centre Estel', type='ecole', description='Centre de formation et d\'accueil pour enfants vulnérables.',
                  contact='+221 77 777 8899',
                  localisation_id=locs[2].id, verifie=True),
        Structure(nom='Orphelinat Alkhayria', type='daara', description='Orphelinat et école coranique à Mbour.',
                  contact='+221 77 333 4455', numero_orange_money='773334455',
                  localisation_id=locs[2].id, verifie=True),
        Structure(nom='Mosquée Omarienne', type='mosquee', description='Grande mosquée de Dakar.',
                  contact='+221 33 822 0000', numero_wave='338220000',
                  localisation_id=locs[0].id, verifie=True),
    ]
    db.session.add_all(structures)
    db.session.flush()

    # ── Annonces dons ─────────────────────────────────────────────────────
    annonces = [
        AnnonceDon(utilisateur_id=user1.id, categorie='habits', sous_categorie='enfants',
                   titre='Lot de 15 vêtements enfants (2-8 ans)', description='Très bon état, lavés et repassés.',
                   localisation_id=locs[0].id, statut='approuve'),
        AnnonceDon(utilisateur_id=user1.id, categorie='habits', sous_categorie='femmes',
                   titre='Robes et pagnes traditionnels',
                   description='5 tenues de fête, tailles 38-42.',
                   localisation_id=locs[1].id, statut='approuve'),
        AnnonceDon(utilisateur_id=user2.id, categorie='alimentation',
                   titre='Sacs de riz (25 kg x3)', description='Riz brisé importé, emballages intacts.',
                   localisation_id=locs[0].id, statut='approuve'),
        AnnonceDon(utilisateur_id=user1.id, categorie='cosmetique',
                   titre='Savons et shampooings', description='Carton de 48 savons Cadum + 12 shampooings.',
                   localisation_id=locs[2].id, statut='approuve'),
        AnnonceDon(utilisateur_id=user2.id, categorie='habits', sous_categorie='hommes',
                   titre='Chemises et pantalons hommes',
                   localisation_id=locs[3].id, statut='en_attente'),
    ]
    db.session.add_all(annonces)
    db.session.flush()

    # ── Missions ──────────────────────────────────────────────────────────
    missions = [
        MissionVolontariat(
            structure_id=structures[2].id, localisation_id=locs[1].id,
            titre='Sensibilisation droits de l\'enfant à Pikine',
            description='Animer des ateliers de sensibilisation dans des écoles de Pikine.',
            competences_requises='Communication, Pédagogie, Français',
            date_debut=date(2025, 9, 1), date_fin=date(2025, 9, 30),
            places_disponibles=5
        ),
        MissionVolontariat(
            structure_id=structures[3].id, localisation_id=locs[0].id,
            titre='Coordination bénévoles CODEVS — Dakar',
            description='Aider à organiser et coordonner les activités de volontariat à Dakar Médina.',
            competences_requises='Organisation, Leadership',
            date_debut=date(2025, 8, 15), date_fin=date(2025, 12, 31),
            places_disponibles=3
        ),
        MissionVolontariat(
            structure_id=structures[4].id, localisation_id=locs[2].id,
            titre='Soutien scolaire — Centre Estel Mbour',
            description='Donner des cours de soutien en mathématiques et français à des enfants de 8-14 ans.',
            competences_requises='Patience, Niveau Bac minimum',
            date_debut=date(2025, 10, 1), date_fin=date(2026, 6, 30),
            places_disponibles=8
        ),
        MissionVolontariat(
            structure_id=structures[5].id, localisation_id=locs[2].id,
            titre='Distribution repas — Orphelinat Alkhayria',
            description='Aider à préparer et distribuer les repas du vendredi pour 80 enfants.',
            competences_requises='Disponibilité le vendredi matin',
            date_debut=date(2025, 8, 1), date_fin=date(2025, 12, 31),
            places_disponibles=10
        ),
    ]
    db.session.add_all(missions)
    db.session.commit()

    print("✅ Base de données peuplée avec succès !")
    print("   Admin : admin@barakasn.sn / admin1234")
    print("   User  : fatou@test.sn / test1234")
