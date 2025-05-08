from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<str:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    
    path("profile/", views.UserProfileView.as_view(), name="user-profile"),
    
    path("categories/", views.CategoryListCreate.as_view(), name="category-list"),
    path("categories/<str:pk>/", views.CategoryDetail.as_view(), name="category-detail"),
    path("tags/", views.TagListCreate.as_view(), name="tag-list"),
    
    path("documents/", views.DocumentListCreate.as_view(), name="document-list"),
    path("documents/<str:pk>/", views.DocumentDetail.as_view(), name="document-detail"),
    path("documents/search/", views.DocumentSearch.as_view(), name="document-search"),
    path("documents/shared/", views.UserSharedDocuments.as_view(), name="shared-documents"),
    path("documents/<str:document_id>/versions/", 
         views.DocumentVersionList.as_view(), name="document-version-list"),
    path("documents/<str:document_id>/shares/", 
         views.DocumentShareListCreate.as_view(), name="document-share-list"),
    path("document-shares/<str:pk>/", 
         views.DocumentShareDetail.as_view(), name="document-share-detail"),
]
