import os
import mimetypes
import hashlib
from django.core.files.storage import default_storage
from django.conf import settings

class FileHandler:
    """Gestionnaire de fichiers pour les documents"""
    
    @staticmethod
    def get_file_info(file_obj):
        """Récupère les informations d'un fichier"""
        file_obj.seek(0, 2)  # Aller à la fin
        size = file_obj.tell()
        file_obj.seek(0)  # Retour au début
        
        content_type, _ = mimetypes.guess_type(file_obj.name)
        if not content_type:
            content_type = 'application/octet-stream'
            
        return {
            'size': size,
            'content_type': content_type,
            'name': file_obj.name
        }
    
    @staticmethod
    def calculate_file_hash(file_obj):
        """Calcule le hash SHA256 d'un fichier"""
        file_obj.seek(0)
        content = file_obj.read()
        file_obj.seek(0)
        return hashlib.sha256(content).hexdigest()
    
    @staticmethod
    def is_duplicate(file_hash):
        """Vérifie si un fichier existe déjà basé sur son hash"""
        from apps.documents.models import Document
        return Document.objects.filter(file_hash=file_hash).exists()