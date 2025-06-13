import logging
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework import status

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception non gérée: {exception}", exc_info=True)
        
        if isinstance(exception, ValidationError):
            return JsonResponse({
                'error': True,
                'message': 'Erreur de validation',
                'details': exception.message_dict if hasattr(exception, 'message_dict') else str(exception)
            }, status=400)
        
        # Pour les erreurs 500
        return JsonResponse({
            'error': True,
            'message': 'Erreur interne du serveur',
            'details': 'Une erreur inattendue s\'est produite'
        }, status=500)