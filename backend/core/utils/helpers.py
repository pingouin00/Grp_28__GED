import hashlib
import mimetypes
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple, Any
import magic

def generate_file_hash(file_content: bytes) -> str:
    """Génère un hash SHA-256 pour le contenu du fichier."""
    return hashlib.sha256(file_content).hexdigest()

def get_file_info(file_obj) -> Tuple[str, str, int]:
    """
    Retourne les informations du fichier: (mime_type, extension, size)
    """
    # Détection du type MIME
    mime = magic.Magic(mime=True)
    file_obj.seek(0)
    content = file_obj.read(1024)
    file_obj.seek(0)
    mime_type = mime.from_buffer(content)
    
    # Extension
    _, extension = os.path.splitext(file_obj.name)
    
    # Taille
    file_obj.seek(0, 2)  # Aller à la fin
    size = file_obj.tell()
    file_obj.seek(0)  # Retour au début
    
    return mime_type, extension.lower(), size

def format_file_size(size_bytes: int) -> str:
    """Formate la taille du fichier en unités lisibles."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def is_file_type_allowed(mime_type: str, allowed_types: list) -> bool:
    """Vérifie si le type de fichier est autorisé."""
    return mime_type in allowed_types

def generate_unique_filename(original_filename: str, user_id: str) -> str:
    """Génère un nom de fichier unique."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_filename)
    return f"{user_id}_{timestamp}_{name}{ext}"

def calculate_expiration_date(days: int = 30) -> datetime:
    """Calcule une date d'expiration."""
    return datetime.now() + timedelta(days=days)