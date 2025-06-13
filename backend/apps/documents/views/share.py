from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.documents.models import Document, DocumentShare
from apps.documents.serializers import DocumentShareSerializer, DocumentListSerializer
from apps.common.permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)

class DocumentShareListCreateView(generics.ListCreateAPIView):
    """Gestion des partages de documents"""
    serializer_class = DocumentShareSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        
        # Seul le propriétaire peut voir les partages
        if document.owner != self.request.user:
            return DocumentShare.objects.none()
            
        return DocumentShare.objects.filter(document=document)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'document_id' in self.kwargs:
            document = get_object_or_404(Document, id=self.kwargs['document_id'])
            context['document'] = document
        return context
    
    def perform_create(self, serializer):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        
        # Vérifier que l'utilisateur est le propriétaire
        if document.owner != self.request.user:
            return Response(
                {'error': 'Permission refusée'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(document=document)

class DocumentShareDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détail d'un partage de document"""
    serializer_class = DocumentShareSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        return DocumentShare.objects.filter(document__owner=user)

class UserSharedDocumentsView(generics.ListAPIView):
    """Documents partagés avec l'utilisateur"""
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(shares__shared_with=self.request.user)