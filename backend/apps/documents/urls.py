from django.urls import path
from .views import (
    DocumentListCreateView, DocumentDetailView,
    CategoryListCreateView, CategoryDetailView,
    TagListCreateView, TagDetailView,
    DocumentDownloadView, DocumentVersionDownloadView,
    DocumentStatisticsView,
    PublicDocumentsView,
    DocumentSearchView,
    DocumentShareListCreateView, DocumentShareDetailView, 
    UserSharedDocumentsView,
    DocumentVersionListCreateView
)

app_name = 'documents'

urlpatterns = [
    # Documents
    path('', DocumentListCreateView.as_view(), name='document-list-create'),
    path('<str:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('<str:document_id>/download/', DocumentDownloadView.as_view(), name='document-download'),
    
    # Versions
    path('<str:document_id>/versions/', DocumentVersionListCreateView.as_view(), name='document-versions'),
    path('<str:document_id>/versions/<str:version_id>/download/', 
         DocumentVersionDownloadView.as_view(), name='version-download'),
    
    # Partages
    path('<str:document_id>/shares/', DocumentShareListCreateView.as_view(), name='document-shares'),
    path('shares/<str:pk>/', DocumentShareDetailView.as_view(), name='document-share-detail'),
    path('shared/', UserSharedDocumentsView.as_view(), name='user-shared-documents'),
    
    # Catégories
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<str:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Tags
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<str:pk>/', TagDetailView.as_view(), name='tag-detail'),
    
    # Fonctionnalités avancées
    path('public/', PublicDocumentsView.as_view(), name='public-documents'),
    path('search/', DocumentSearchView.as_view(), name='document-search'),
    path('statistics/', DocumentStatisticsView.as_view(), name='document-statistics'),
]