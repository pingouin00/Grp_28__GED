from django.core.exceptions import ValidationError
import os
import magic
from core.utils.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, ALLOWED_FILE_TYPES

def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Extension non autorisée. Extensions autorisées: {ALLOWED_EXTENSIONS}')

def validate_file_size(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(f'Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE/1024/1024}MB')

def validate_file_type(file):
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file.read(1024))
        file.seek(0)
        if file_type not in ALLOWED_FILE_TYPES:
            raise ValidationError(f'Type de fichier non autorisé: {file_type}')
    except Exception as e:
        raise ValidationError(f'Erreur lors de la validation du type de fichier: {str(e)}')