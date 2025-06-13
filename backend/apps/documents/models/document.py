from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField
from apps.common.models import TimeStampedModel
from .category import Category
from .tag import Tag
from core.database.gridfs import GridFSManager
import logging

logger = logging.getLogger(__name__)

class Document(TimeStampedModel):
    id = ObjectIdField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    gridfs_file_id = models.CharField(max_length=100, blank=True, null=True)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    file_size = models.PositiveIntegerField()
    file_hash = models.CharField(max_length=64, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="documents", null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="documents", blank=True)
    is_public = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['is_public', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['file_hash']),
        ]

    def __str__(self):
        return self.title

    def save_file_to_gridfs(self, file_obj):
        """Sauvegarde un fichier dans GridFS"""
        gridfs_manager = GridFSManager()
        return gridfs_manager.save_file(file_obj, self)

    def get_file_from_gridfs(self):
        """Récupère un fichier depuis GridFS"""
        if not self.gridfs_file_id:
            return None
        
        gridfs_manager = GridFSManager()
        file_obj = gridfs_manager.get_file(self.gridfs_file_id)
        
        if file_obj:
            self.download_count += 1
            self.save(update_fields=['download_count'])
        
        return file_obj

    def delete_file_from_gridfs(self):
        """Supprime un fichier de GridFS"""
        if not self.gridfs_file_id:
            return
        
        gridfs_manager = GridFSManager()
        gridfs_manager.delete_file(self.gridfs_file_id, self)

    def delete(self, *args, **kwargs):
        """Override delete pour supprimer aussi le fichier GridFS"""
        self.delete_file_from_gridfs()
        super().delete(*args, **kwargs)