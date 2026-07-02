import os
from dotenv import load_dotenv

load_dotenv()

# Render génère des URLs qui commencent par "postgres://"
# mais SQLAlchemy exige "postgresql://" — on corrige automatiquement
database_url = os.environ.get('DATABASE_URL') or 'sqlite:///barakasn.db'
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app/static/img/uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload