from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField
from apps.common.models import TimeStampedModel

class Note(TimeStampedModel):
    id = ObjectIdField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
        ]
    
    def __str__(self):
        return self.title