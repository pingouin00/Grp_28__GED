from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.documents.models import Document, DocumentVersion
from apps.documents.serializers import DocumentVersionSerializer
import logging

logger = logging.getLogger(__name__)

class DocumentVersionListCreateView(generics.ListCreateAPIView):
    """Gestion des versions de documents"""
    serializer_class = DocumentVersionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        user = self.request.user
        
        # Vérifier les permissions
        has_permission = (
            document.owner == user or 
            document.shares.filter(shared_with=user).exists() or 
            document.is_public
        )
        
        if not has_permission:
            return DocumentVersion.objects.none()
            
        return DocumentVersion.objects.filter(document=document)
    
    def perform_create(self, serializer):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        user = self.request.user
        
        # Vérifier les permissions d'édition
        can_edit = (
            document.owner == user or 
            document.shares.filter(shared_with=user, can_edit=True).exists()
        )
        
        if not can_edit:
            return Response(
                {'error': 'Permission de modification refusée'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Calculer le numéro de version
        latest_version = document.versions.order_by('-version_number').first()
        version_number = 1 if not latest_version else latest_version.version_number + 1
        
        serializer.save(
            document=document,
            created_by=user,
            version_number=version_number
        )