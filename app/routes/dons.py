from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import AnnonceDon, Structure, PromesseDon, Localisation
from app.utils import save_image, delete_image

dons_bp = Blueprint('dons', __name__)

# ── Habits ────────────────────────────────────────────────────────────────────

@dons_bp.route('/habits')
def habits():
    sous_cat = request.args.get('sous_categorie', '')
    query = AnnonceDon.query.filter_by(categorie='habits', statut='approuve')
    if sous_cat:
        query = query.filter_by(sous_categorie=sous_cat)
    annonces = query.order_by(AnnonceDon.created_at.desc()).all()
    return render_template('dons/habits.html', annonces=annonces, filtre=sous_cat)

# ── Produits ──────────────────────────────────────────────────────────────────

@dons_bp.route('/produits')
def produits():
    sous_cat = request.args.get('sous_categorie', '')
    query = AnnonceDon.query.filter(
        AnnonceDon.categorie.in_(['alimentation', 'cosmetique']),
        AnnonceDon.statut == 'approuve'
    )
    if sous_cat:
        query = query.filter_by(categorie=sous_cat)
    annonces = query.order_by(AnnonceDon.created_at.desc()).all()
    return render_template('dons/produits.html', annonces=annonces, filtre=sous_cat)

# ── Argent ────────────────────────────────────────────────────────────────────

@dons_bp.route('/argent')
def argent():
    type_str = request.args.get('type', '')
    query = Structure.query.filter_by(verifie=True)
    if type_str:
        query = query.filter_by(type=type_str)
    structures = query.all()
    return render_template('dons/argent.html', structures=structures, filtre=type_str)

@dons_bp.route('/argent/<int:structure_id>/promettre', methods=['POST'])
@login_required
def promettre(structure_id):
    structure = Structure.query.get_or_404(structure_id)
    montant = request.form.get('montant')
    operateur = request.form.get('operateur')
    if not montant or float(montant) < 100:
        flash('Montant invalide (minimum 100 FCFA).', 'danger')
        return redirect(url_for('dons.argent'))
    promesse = PromesseDon(
        utilisateur_id=current_user.id,
        structure_id=structure.id,
        montant=float(montant),
        operateur=operateur
    )
    db.session.add(promesse)
    db.session.commit()
    flash(f'✅ Promesse de {int(float(montant)):,} FCFA enregistrée via {operateur.replace("_"," ").title()} !', 'success')
    return redirect(url_for('dons.argent'))

# ── Détail annonce ────────────────────────────────────────────────────────────

@dons_bp.route('/annonce/<int:id>')
def detail_annonce(id):
    annonce = AnnonceDon.query.get_or_404(id)
    if annonce.statut != 'approuve':
        flash("Cette annonce n'est pas encore disponible.", 'warning')
        return redirect(url_for('main.index'))
    return render_template('dons/detail_annonce.html', annonce=annonce)

# ── Créer une annonce ─────────────────────────────────────────────────────────

@dons_bp.route('/annonce/creer', methods=['GET', 'POST'])
@login_required
def creer_annonce():
    localisations = Localisation.query.order_by(Localisation.region, Localisation.ville).all()
    if request.method == 'POST':
        # Upload image optionnelle
        image_filename = None
        if 'image' in request.files:
            image_filename = save_image(request.files['image'])

        annonce = AnnonceDon(
            utilisateur_id=current_user.id,
            categorie=request.form.get('categorie'),
            sous_categorie=request.form.get('sous_categorie') or None,
            titre=request.form.get('titre'),
            description=request.form.get('description'),
            localisation_id=request.form.get('localisation_id') or None,
            image=image_filename,
        )
        db.session.add(annonce)
        db.session.commit()
        flash('📢 Annonce soumise ! Elle sera visible après modération (sous 24h).', 'success')
        return redirect(url_for('auth.mon_espace'))
    return render_template('dons/creer_annonce.html', localisations=localisations)

# ── Supprimer une annonce (propriétaire ou admin) ─────────────────────────────

@dons_bp.route('/annonce/<int:id>/supprimer', methods=['POST'])
@login_required
def supprimer_annonce(id):
    annonce = AnnonceDon.query.get_or_404(id)
    if annonce.utilisateur_id != current_user.id and not current_user.is_admin():
        flash("Action non autorisée.", 'danger')
        return redirect(url_for('auth.mon_espace'))
    delete_image(annonce.image)
    db.session.delete(annonce)
    db.session.commit()
    flash('Annonce supprimée.', 'warning')
    return redirect(url_for('auth.mon_espace'))

# ── Marquer comme terminé ─────────────────────────────────────────────────────

@dons_bp.route('/annonce/<int:id>/terminer', methods=['POST'])
@login_required
def terminer_annonce(id):
    annonce = AnnonceDon.query.get_or_404(id)
    if annonce.utilisateur_id != current_user.id and not current_user.is_admin():
        flash("Action non autorisée.", 'danger')
        return redirect(url_for('auth.mon_espace'))
    annonce.statut = 'termine'
    db.session.commit()
    flash('✅ Annonce marquée comme terminée.', 'success')
    return redirect(url_for('auth.mon_espace'))
