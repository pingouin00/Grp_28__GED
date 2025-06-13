from django.urls import path
from .views import NoteListCreateView, NoteDetailView

app_name = 'notes'

urlpatterns = [
    path('', NoteListCreateView.as_view(), name='note-list-create'),
    path('<str:pk>/', NoteDetailView.as_view(), name='note-detail'),
]