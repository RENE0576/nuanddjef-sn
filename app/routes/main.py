from flask import Blueprint, render_template
from app.models import AnnonceDon, Structure, MissionVolontariat

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    stats = {
        'annonces': AnnonceDon.query.filter_by(statut='approuve').count(),
        'structures': Structure.query.filter_by(verifie=True).count(),
        'missions': MissionVolontariat.query.filter_by(active=True).count(),
    }
    dernieres_annonces = AnnonceDon.query.filter_by(statut='approuve').order_by(AnnonceDon.created_at.desc()).limit(6).all()
    return render_template('index.html', stats=stats, dernieres_annonces=dernieres_annonces)
