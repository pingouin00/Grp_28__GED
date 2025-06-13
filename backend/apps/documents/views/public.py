from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.documents.models import Document
from apps.documents.serializers import DocumentListSerializer

class PublicDocumentsView(generics.ListAPIView):
    """Documents publics accessibles à tous les utilisateurs connectés"""
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(is_public=True)