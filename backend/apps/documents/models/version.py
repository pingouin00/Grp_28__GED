from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField
from apps.common.models import TimeStampedModel
from core.database.gridfs import GridFSManager
import logging

logger = logging.getLogger(__name__)

class DocumentVersion(TimeStampedModel):
    id = ObjectIdField(primary_key=True)
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE, related_name="versions")
    gridfs_file_id = models.CharField(max_length=100)
    version_number = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="document_versions")
    comments = models.TextField(blank=True, null=True)
    file_size = models.PositiveIntegerField(default=0)
    file_hash = models.CharField(max_length=64, blank=True, null=True)
    
    class Meta:
        unique_together = ['document', 'version_number']
        ordering = ['-version_number']
        indexes = [
            models.Index(fields=['document', '-version_number']),
        ]
    
    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"
    
    def save_version_to_gridfs(self, file_obj):
        gridfs_manager = GridFSManager()
        return gridfs_manager.save_version(file_obj, self)
    
    def get_version_from_gridfs(self):
        if not self.gridfs_file_id:
            return None
        gridfs_manager = GridFSManager()
        return gridfs_manager.get_file(self.gridfs_file_id)
    
    def delete(self, *args, **kwargs):
        if self.gridfs_file_id:
            gridfs_manager = GridFSManager()
            gridfs_manager.delete_version(self.gridfs_file_id, self)
        super().delete(*args, **kwargs)