from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField
from apps.common.models import TimeStampedModel
from datetime import datetime

class DocumentShare(TimeStampedModel):
    id = ObjectIdField(primary_key=True)
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE, related_name="shares")
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_documents")
    can_edit = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['document', 'shared_with']
        indexes = [
            models.Index(fields=['shared_with', '-created_at']),
            models.Index(fields=['document', 'shared_with']),
        ]
    
    def __str__(self):
        return f"{self.document.title} partagé avec {self.shared_with.username}"
    
    def is_expired(self):
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False