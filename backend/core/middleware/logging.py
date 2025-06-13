import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        
        # Log des requêtes importantes
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            logger.info(f"{request.method} {request.path} - User: {getattr(request.user, 'username', 'Anonymous')}")

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log des réponses lentes
            if duration > 1.0:  # Plus d'1 seconde
                logger.warning(f"Requête lente: {request.method} {request.path} - {duration:.2f}s")
            
            # Log des erreurs
            if response.status_code >= 400:
                logger.error(f"Erreur {response.status_code}: {request.method} {request.path}")
        
        return response