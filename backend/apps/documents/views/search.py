from django.db.models import Q
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from apps.documents.models import Document
from apps.documents.serializers import DocumentListSerializer

class DocumentSearchView(generics.ListAPIView):
    """Recherche avancée dans les documents"""
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__name', 'category__name']
    
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(
            Q(owner=user) | Q(shares__shared_with=user) | Q(is_public=True)
        ).distinct()