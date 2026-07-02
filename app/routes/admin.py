from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import AnnonceDon, Structure, MissionVolontariat, Localisation, Candidature

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Accès réservé aux administrateurs.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'annonces_attente': AnnonceDon.query.filter_by(statut='en_attente').count(),
        'structures': Structure.query.count(),
        'missions': MissionVolontariat.query.count(),
        'candidatures': Candidature.query.filter_by(statut='en_attente').count(),
    }
    return render_template('admin/dashboard.html', stats=stats)

# ── Modération des annonces ───────────────────────────────────────────────────

@admin_bp.route('/annonces')
@login_required
@admin_required
def annonces():
    statut = request.args.get('statut', 'en_attente')
    annonces = AnnonceDon.query.filter_by(statut=statut).order_by(AnnonceDon.created_at.desc()).all()
    return render_template('admin/annonces.html', annonces=annonces, statut_filtre=statut)

@admin_bp.route('/annonces/<int:id>/approuver', methods=['POST'])
@login_required
@admin_required
def approuver_annonce(id):
    annonce = AnnonceDon.query.get_or_404(id)
    annonce.statut = 'approuve'
    db.session.commit()
    flash('Annonce approuvée.', 'success')
    return redirect(url_for('admin.annonces'))

@admin_bp.route('/annonces/<int:id>/rejeter', methods=['POST'])
@login_required
@admin_required
def rejeter_annonce(id):
    annonce = AnnonceDon.query.get_or_404(id)
    annonce.statut = 'rejete'
    db.session.commit()
    flash('Annonce rejetée.', 'warning')
    return redirect(url_for('admin.annonces'))

# ── Gestion des structures ────────────────────────────────────────────────────

@admin_bp.route('/structures')
@login_required
@admin_required
def structures():
    structures = Structure.query.order_by(Structure.type, Structure.nom).all()
    return render_template('admin/structures.html', structures=structures)

@admin_bp.route('/structures/ajouter', methods=['GET', 'POST'])
@login_required
@admin_required
def ajouter_structure():
    localisations = Localisation.query.order_by(Localisation.region, Localisation.ville).all()
    if request.method == 'POST':
        structure = Structure(
            nom=request.form.get('nom'),
            type=request.form.get('type'),
            description=request.form.get('description'),
            contact=request.form.get('contact'),
            numero_orange_money=request.form.get('numero_orange_money'),
            numero_wave=request.form.get('numero_wave'),
            localisation_id=request.form.get('localisation_id') or None,
            verifie=True
        )
        db.session.add(structure)
        db.session.commit()
        flash('Structure ajoutée avec succès.', 'success')
        return redirect(url_for('admin.structures'))
    return render_template('admin/ajouter_structure.html', localisations=localisations)

@admin_bp.route('/structures/<int:id>/supprimer', methods=['POST'])
@login_required
@admin_required
def supprimer_structure(id):
    structure = Structure.query.get_or_404(id)
    db.session.delete(structure)
    db.session.commit()
    flash('Structure supprimée.', 'warning')
    return redirect(url_for('admin.structures'))

# ── Gestion des missions ──────────────────────────────────────────────────────

@admin_bp.route('/missions')
@login_required
@admin_required
def missions():
    missions = MissionVolontariat.query.order_by(MissionVolontariat.date_debut.desc()).all()
    return render_template('admin/missions.html', missions=missions)

@admin_bp.route('/missions/ajouter', methods=['GET', 'POST'])
@login_required
@admin_required
def ajouter_mission():
    structures = Structure.query.filter_by(verifie=True).order_by(Structure.nom).all()
    localisations = Localisation.query.order_by(Localisation.region, Localisation.ville).all()
    if request.method == 'POST':
        from datetime import date
        def parse_date(s):
            try: return date.fromisoformat(s) if s else None
            except: return None
        mission = MissionVolontariat(
            titre=request.form.get('titre'),
            structure_id=request.form.get('structure_id'),
            description=request.form.get('description'),
            competences_requises=request.form.get('competences_requises'),
            date_debut=parse_date(request.form.get('date_debut')),
            date_fin=parse_date(request.form.get('date_fin')),
            places_disponibles=int(request.form.get('places_disponibles') or 5),
            localisation_id=request.form.get('localisation_id') or None,
            active=True
        )
        db.session.add(mission)
        db.session.commit()
        flash('Mission créée avec succès.', 'success')
        return redirect(url_for('admin.missions'))
    return render_template('admin/ajouter_mission.html',
                           structures=structures, localisations=localisations)

@admin_bp.route('/missions/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_mission(id):
    mission = MissionVolontariat.query.get_or_404(id)
    mission.active = not mission.active
    db.session.commit()
    etat = 'activée' if mission.active else 'désactivée'
    flash(f'Mission {etat}.', 'success')
    return redirect(url_for('admin.missions'))

@admin_bp.route('/missions/<int:id>/supprimer', methods=['POST'])
@login_required
@admin_required
def supprimer_mission(id):
    mission = MissionVolontariat.query.get_or_404(id)
    db.session.delete(mission)
    db.session.commit()
    flash('Mission supprimée.', 'warning')
    return redirect(url_for('admin.missions'))

# ── Gestion des candidatures ──────────────────────────────────────────────────

@admin_bp.route('/candidatures')
@login_required
@admin_required
def candidatures():
    from app.models import Candidature
    statut = request.args.get('statut', 'en_attente')
    candidatures = Candidature.query.filter_by(statut=statut)\
        .order_by(Candidature.created_at.desc()).all()
    return render_template('admin/candidatures.html',
                           candidatures=candidatures, statut_filtre=statut)

@admin_bp.route('/candidatures/<int:id>/accepter', methods=['POST'])
@login_required
@admin_required
def accepter_candidature(id):
    from app.models import Candidature
    c = Candidature.query.get_or_404(id)
    c.statut = 'accepte'
    # Décrémenter les places
    if c.mission.places_disponibles > 0:
        c.mission.places_disponibles -= 1
    db.session.commit()
    flash('Candidature acceptée.', 'success')
    return redirect(url_for('admin.candidatures'))

@admin_bp.route('/candidatures/<int:id>/refuser', methods=['POST'])
@login_required
@admin_required
def refuser_candidature(id):
    from app.models import Candidature
    c = Candidature.query.get_or_404(id)
    c.statut = 'refuse'
    db.session.commit()
    flash('Candidature refusée.', 'warning')
    return redirect(url_for('admin.candidatures'))

# ── Gestion des localisations ─────────────────────────────────────────────────

@admin_bp.route('/localisations')
@login_required
@admin_required
def localisations():
    locs = Localisation.query.order_by(Localisation.region, Localisation.ville).all()
    return render_template('admin/localisations.html', localisations=locs)

@admin_bp.route('/localisations/ajouter', methods=['POST'])
@login_required
@admin_required
def ajouter_localisation():
    loc = Localisation(
        region=request.form.get('region'),
        ville=request.form.get('ville'),
        quartier=request.form.get('quartier') or None
    )
    db.session.add(loc)
    db.session.commit()
    flash('Localisation ajoutée.', 'success')
    return redirect(url_for('admin.localisations'))

@admin_bp.route('/localisations/<int:id>/supprimer', methods=['POST'])
@login_required
@admin_required
def supprimer_localisation(id):
    loc = Localisation.query.get_or_404(id)
    db.session.delete(loc)
    db.session.commit()
    flash('Localisation supprimée.', 'warning')
    return redirect(url_for('admin.localisations'))
