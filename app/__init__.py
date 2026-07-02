from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Créer le dossier uploads s'il n'existe pas
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'app/static/img/uploads'), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'warning'

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dons import dons_bp
    from app.routes.volontariat import volontariat_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dons_bp, url_prefix='/dons')
    app.register_blueprint(volontariat_bp, url_prefix='/volontariat')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # ── Gestionnaires d'erreurs ───────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # ── Filtre Jinja utilitaire ───────────────────────────────────────────
    @app.template_filter('date_fr')
    def date_fr(d):
        if not d: return '—'
        mois = ['jan','fév','mar','avr','mai','jun','jul','aoû','sep','oct','nov','déc']
        return f"{d.day} {mois[d.month-1]} {d.year}"

    return app
