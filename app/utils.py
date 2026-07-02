import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    """Sauvegarde une image uploadée et retourne le nom de fichier unique."""
    if not file or file.filename == '':
        return None
    if not allowed_file(file.filename):
        return None
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/img/uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, filename))
    return filename

def delete_image(filename):
    """Supprime une image uploadée du disque."""
    if not filename:
        return
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/img/uploads')
    path = os.path.join(upload_folder, filename)
    if os.path.exists(path):
        os.remove(path)
