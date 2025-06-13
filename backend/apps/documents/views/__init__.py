from .document import DocumentListCreateView, DocumentDetailView
from .category import CategoryListCreateView, CategoryDetailView
from .tag import TagListCreateView, TagDetailView
from .download import download_document

__all__ = [
    'DocumentListCreateView', 'DocumentDetailView',
    'CategoryListCreateView', 'CategoryDetailView',
    'TagListCreateView', 'TagDetailView',
    'download_document'
]