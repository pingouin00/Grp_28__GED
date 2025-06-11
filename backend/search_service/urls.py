from django.urls import path
from .views import search_documents

urlpatterns = [
    path('documents/', search_documents, name='search_documents'),
]
