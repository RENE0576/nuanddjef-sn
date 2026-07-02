from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import MissionVolontariat, Candidature, Localisation

volontariat_bp = Blueprint('volontariat', __name__)

@volontariat_bp.route('/')
def index():
    region = request.args.get('region', '')
    ville = request.args.get('ville', '')
    quartier = request.args.get('quartier', '')

    query = MissionVolontariat.query.filter_by(active=True)
    if region or ville or quartier:
        query = query.join(Localisation)
        if region:
            query = query.filter(Localisation.region == region)
        if ville:
            query = query.filter(Localisation.ville == ville)
        if quartier:
            query = query.filter(Localisation.quartier == quartier)

    missions = query.order_by(MissionVolontariat.date_debut).all()
    regions = db.session.query(Localisation.region).distinct().order_by(Localisation.region).all()
    return render_template('volontariat/index.html', missions=missions,
                           regions=[r[0] for r in regions],
                           filtres={'region': region, 'ville': ville, 'quartier': quartier})

@volontariat_bp.route('/<int:mission_id>')
def detail(mission_id):
    mission = MissionVolontariat.query.get_or_404(mission_id)
    deja_candidat = False
    if current_user.is_authenticated:
        deja_candidat = Candidature.query.filter_by(
            utilisateur_id=current_user.id, mission_id=mission_id).first() is not None
    return render_template('volontariat/detail.html', mission=mission, deja_candidat=deja_candidat)

@volontariat_bp.route('/<int:mission_id>/postuler', methods=['POST'])
@login_required
def postuler(mission_id):
    mission = MissionVolontariat.query.get_or_404(mission_id)
    if Candidature.query.filter_by(utilisateur_id=current_user.id, mission_id=mission_id).first():
        flash('Vous avez déjà postulé à cette mission.', 'warning')
        return redirect(url_for('volontariat.detail', mission_id=mission_id))
    candidature = Candidature(
        utilisateur_id=current_user.id,
        mission_id=mission_id,
        message=request.form.get('message')
    )
    db.session.add(candidature)
    db.session.commit()
    flash('Candidature envoyée avec succès !', 'success')
    return redirect(url_for('auth.mon_espace'))
