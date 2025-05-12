from django.shortcuts import render , get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status , filters
from rest_framework.response import Response
from .serializers import (
    UserSerializer, NoteSerializer, UserProfileSerializer, UserUpdateSerializer,
    DocumentListSerializer, DocumentDetailSerializer, CategorySerializer,
    TagSerializer, DocumentVersionSerializer, DocumentShareSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, Document, Category, Tag, DocumentVersion, DocumentShare
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
 
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profil mis à jour avec succès"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
     
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)# get notes of the user

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Note.objects.all() 

class NoteDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Note.objects.all()

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(created_by=user)

class TagListCreate(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Tag.objects.all()

class DocumentListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'tags__name', 'category__name']
    filterset_fields = {
        'category': ['exact'],
        'tags': ['exact'],
        'created_at': ['gte', 'lte'],
        'is_public': ['exact'],
    }
    ordering_fields = ['title', 'created_at', 'updated_at', 'file_size']
    ordering = ['-created_at']

    def get_serializer_class(self):
        return DocumentListSerializer if self.request.method == 'GET' else DocumentDetailSerializer

    def get_queryset(self):
        user = self.request.user
        # Documents owned by user or shared with user
        return Document.objects.filter(
            Q(owner=user) | Q(shares__shared_with=user) | Q(is_public=True)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentDetailSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        # Documents owned by user or shared with user
        return Document.objects.filter(
            Q(owner=user) | Q(shares__shared_with=user) | Q(is_public=True)
        ).distinct()
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        # Vérifier si l'utilisateur a le droit de modifier le document
        if request.method not in ['GET', 'HEAD', 'OPTIONS']:
            if obj.owner != request.user and not obj.shares.filter(shared_with=request.user, can_edit=True).exists():
                self.permission_denied(request, message="Vous n'avez pas la permission de modifier ce document.")

class DocumentVersionList(generics.ListCreateAPIView):
    serializer_class = DocumentVersionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        
        # Vérifier si l'utilisateur a accès au document
        user = self.request.user
        if document.owner != user and not document.shares.filter(shared_with=user).exists() and not document.is_public:
            return DocumentVersion.objects.none()
            
        return DocumentVersion.objects.filter(document=document)
    
    def perform_create(self, serializer):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        
        # Vérifier si l'utilisateur a le droit de créer une version
        user = self.request.user
        if document.owner != user and not document.shares.filter(shared_with=user, can_edit=True).exists():
            self.permission_denied(self.request, message="Vous n'avez pas la permission de créer une version pour ce document.")
        
        # Déterminer le numéro de version
        latest_version = document.versions.order_by('-version_number').first()
        version_number = 1 if not latest_version else latest_version.version_number + 1
        
        serializer.save(
            document=document,
            created_by=user,
            version_number=version_number
        )

class DocumentShareListCreate(generics.ListCreateAPIView):
    serializer_class = DocumentShareSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        document = get_object_or_404(Document, id=document_id)
        
        # Vérifier si l'utilisateur est propriétaire du document
        if document.owner != self.request.user:
            return DocumentShare.objects.none()
            
        return DocumentShare.objects.filter(document=document)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'document_id' in self.kwargs:
            document = get_object_or_404(Document, id=self.kwargs['document_id'])
            context['document'] = document
        return context

class DocumentShareDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentShareSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Partages des documents possédés par l'utilisateur
        return DocumentShare.objects.filter(document__owner=user)

class UserSharedDocuments(generics.ListAPIView):
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(shares__shared_with=self.request.user)

class DocumentSearch(generics.ListAPIView):
    serializer_class = DocumentListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__name', 'category__name']

    def get_queryset(self):
        user = self.request.user
        # Documents owned by user or shared with user or public
        return Document.objects.filter(
            Q(owner=user) | Q(shares__shared_with=user) | Q(is_public=True)
        ).distinct()
