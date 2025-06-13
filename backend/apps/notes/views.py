from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Note
from .serializers import NoteListSerializer, NoteDetailSerializer ,NoteCreateSerializer, NoteUpdateSerializer
from apps.common.permissions import IsOwnerOrReadOnly

class NoteListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        return NoteListSerializer if self.request.method == 'GET' else NoteDetailSerializer
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
    
class NoteCreateView(generics.CreateAPIView):
    serializer_class = NoteCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NoteUpdateView(generics.UpdateAPIView):
    serializer_class = NoteUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Note.objects.all()