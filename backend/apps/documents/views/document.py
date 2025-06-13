from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ..models import Document
from ..serializers import DocumentListSerializer, DocumentDetailSerializer
from ..permissions import IsOwnerOrSharedWith
from ..filters import DocumentFilter

class DocumentListCreateView(generics.ListCreateAPIView):
    """Liste et création de documents"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DocumentFilter
    search_fields = ['title', 'description', 'tags__name', 'category__name']
    ordering_fields = ['title', 'created_at', 'updated_at', 'file_size']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        return DocumentListSerializer if self.request.method == 'GET' else DocumentDetailSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(
            Q(owner=user) | Q(shares__shared_with=user) | Q(is_public=True)
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détail, modification et suppression de document"""
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSharedWith]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(
            Q(owner=user) | Q(shares__shared_with=user) | Q(is_public=True)
        ).distinct()