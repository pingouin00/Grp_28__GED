from django.db import models
from django_mongodb_backend.fields import ObjectIdField
from apps.common.models import TimeStampedModel

class Tag(TimeStampedModel):
    id = ObjectIdField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name