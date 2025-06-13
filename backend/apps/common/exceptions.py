from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Gestionnaire d'exceptions personnalisé"""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'Une erreur est survenue',
            'details': response.data
        }
        
        # Log de l'erreur
        logger.error(f"Exception: {exc}, Context: {context}")
        
        response.data = custom_response_data
    
    return response

class GridFSError(Exception):
    """Exception pour les erreurs GridFS"""
    pass

class FileValidationError(Exception):
    """Exception pour les erreurs de validation de fichier"""
    pass