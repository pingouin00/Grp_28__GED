from django.http import Http404, StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.documents.models import Document, DocumentVersion
import logging

logger = logging.getLogger(__name__)

@method_decorator(cache_control(max_age=3600), name='dispatch')
class DocumentDownloadView(LoginRequiredMixin, View):
    """Téléchargement sécurisé de documents depuis GridFS"""
    
    def get(self, request, document_id):
        try:
            document = self._get_accessible_document(request.user, document_id)
            
            # Vérifier l'expiration des partages
            self._check_share_expiration(document, request.user)
            
            # Récupérer le fichier depuis GridFS
            gridfs_file = document.get_file_from_gridfs()
            if not gridfs_file:
                raise Http404("Fichier non trouvé dans le stockage")
            
            # Incrémenter le compteur de téléchargements
            Document.objects.filter(id=document_id).update(
                download_count=models.F('download_count') + 1
            )
            
            return self._create_streaming_response(gridfs_file, document)
            
        except Document.DoesNotExist:
            raise Http404("Document non trouvé")
        except Exception as e:
            logger.error(f"Erreur téléchargement document {document_id}: {str(e)}")
            raise Http404("Erreur lors du téléchargement")
    
    def _get_accessible_document(self, user, document_id):
        """Récupère un document accessible par l'utilisateur"""
        document = get_object_or_404(Document, id=document_id)
        
        has_permission = (
            document.owner == user or 
            document.is_public or
            document.shares.filter(shared_with=user).exists()
        )
        
        if not has_permission:
            raise Http404("Document non trouvé")
            
        return document
    
    def _check_share_expiration(self, document, user):
        """Vérifie si les partages ne sont pas expirés"""
        if hasattr(document, 'shares'):
            shared = document.shares.filter(shared_with=user).first()
            if shared and shared.is_expired():
                raise Http404("Le lien de partage a expiré")
    
    def _create_streaming_response(self, gridfs_file, document):
        """Crée une réponse de streaming pour le téléchargement"""
        def file_iterator(file_obj, chunk_size=8192):
            try:
                while True:
                    chunk = file_obj.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            finally:
                file_obj.close()
        
        response = StreamingHttpResponse(
            file_iterator(gridfs_file),
            content_type=document.file_type or 'application/octet-stream'
        )
        
        response['Content-Disposition'] = f'attachment; filename="{document.original_filename}"'
        response['Content-Length'] = str(document.file_size)
        response['Cache-Control'] = 'private, max-age=3600'
        
        return response

class DocumentVersionDownloadView(DocumentDownloadView):
    """Téléchargement de versions spécifiques de documents"""
    
    def get(self, request, document_id, version_id):
        try:
            document = self._get_accessible_document(request.user, document_id)
            version = get_object_or_404(
                DocumentVersion, 
                id=version_id, 
                document=document
            )
            
            self._check_share_expiration(document, request.user)
            
            gridfs_file = version.get_version_from_gridfs()
            if not gridfs_file:
                raise Http404("Version non trouvée dans le stockage")
            
            return self._create_version_streaming_response(gridfs_file, document, version)
            
        except (Document.DoesNotExist, DocumentVersion.DoesNotExist):
            raise Http404("Version non trouvée")
        except Exception as e:
            logger.error(f"Erreur téléchargement version {version_id}: {str(e)}")
            raise Http404("Erreur lors du téléchargement de la version")
    
    def _create_version_streaming_response(self, gridfs_file, document, version):
        """Crée une réponse de streaming pour une version"""
        def file_iterator(file_obj, chunk_size=8192):
            try:
                while True:
                    chunk = file_obj.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            finally:
                file_obj.close()
        
        response = StreamingHttpResponse(
            file_iterator(gridfs_file),
            content_type=gridfs_file.metadata.get('content_type', 'application/octet-stream')
        )
        
        filename = f"{document.title}_v{version.version_number}_{gridfs_file.filename}"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = str(version.file_size)
        response['Cache-Control'] = 'private, max-age=3600'
        
        return response