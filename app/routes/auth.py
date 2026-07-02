from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Utilisateur

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'donateur')

        if Utilisateur.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('auth.inscription'))

        user = Utilisateur(nom=nom, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès ! Connectez-vous.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/inscription.html')

@auth_bp.route('/connexion', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Utilisateur.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        flash('Email ou mot de passe incorrect.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/deconnexion')
@login_required
def deconnexion():
    flash("Vous avez été déconnecté.", "success")
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/mon-espace')
@login_required
def mon_espace():
    return render_template('auth/mon_espace.html')
