import hashlib
import mimetypes
from django.core.files.storage import default_storage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def generate_file_hash(file_content):
    """Génère un hash SHA256 pour un contenu de fichier"""
    return hashlib.sha256(file_content).hexdigest()

def get_content_type(filename):
    """Détermine le type MIME d'un fichier"""
    content_type, encoding = mimetypes.guess_type(filename)
    return content_type or 'application/octet-stream'

def format_file_size(size_bytes):
    """Formate une taille de fichier en format lisible"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def validate_file_upload(file_obj):
    """Valide un fichier uploadé"""
    from .validators import validate_file_size, validate_file_extension, validate_file_type
    
    try:
        validate_file_size(file_obj)
        validate_file_extension(file_obj)
        validate_file_type(file_obj)
        return True, None
    except Exception as e:
        logger.error(f"Validation failed for file {file_obj.name}: {str(e)}")
        return False, str(e)