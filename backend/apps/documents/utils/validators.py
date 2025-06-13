import magic
from django.core.exceptions import ValidationError
from django.conf import settings

ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.png', '.zip']
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def validate_file_extension(file):
    """Valide l'extension du fichier"""
    import os
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Extension non autorisée. Extensions autorisées: {ALLOWED_EXTENSIONS}')

def validate_file_size(file):
    """Valide la taille du fichier"""
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(f'Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE/1024/1024}MB')

def validate_file_type(file):
    """Valide le type MIME du fichier"""
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file.read(1024))
        file.seek(0)  # Reset file pointer
        
        # Liste des types MIME autorisés
        allowed_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain',
            'image/jpeg',
            'image/png',
            'application/zip'
        ]
        
        if file_type not in allowed_types:
            raise ValidationError(f'Type de fichier non autorisé: {file_type}')
    except Exception as e:
        raise ValidationError(f'Erreur lors de la validation du type de fichier: {str(e)}')