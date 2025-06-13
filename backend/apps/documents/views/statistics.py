from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.documents.models import Document, Category
from apps.documents.serializers import DocumentListSerializer
import logging

logger = logging.getLogger(__name__)

class DocumentStatisticsView(APIView):
    """Statistiques des documents pour l'utilisateur connecté"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            # Statistiques générales
            total_documents = Document.objects.filter(owner=user).count()
            total_size = Document.objects.filter(owner=user).aggregate(
                total=models.Sum('file_size')
            )['total'] or 0
            
            # Statistiques par catégorie
            categories_stats = Category.objects.filter(created_by=user).annotate(
                doc_count=models.Count('documents')
            ).values('name', 'doc_count')
            
            # Documents récents et populaires
            recent_docs = Document.objects.filter(owner=user)\
                .order_by('-created_at')[:5]
            popular_docs = Document.objects.filter(owner=user)\
                .order_by('-download_count')[:5]
            
            return Response({
                'total_documents': total_documents,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'categories_stats': list(categories_stats),
                'recent_documents': DocumentListSerializer(
                    recent_docs, many=True, context={'request': request}
                ).data,
                'popular_documents': DocumentListSerializer(
                    popular_docs, many=True, context={'request': request}
                ).data,
            })
            
        except Exception as e:
            logger.error(f"Erreur récupération statistiques: {str(e)}")
            return Response(
                {'error': 'Erreur lors de la récupération des statistiques'}, 
                status=500
            )