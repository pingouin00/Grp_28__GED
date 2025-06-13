from django.db import models
from django_mongodb_backend.fields import ObjectIdField

class TimeStampedModel(models.Model):
    """Modèle abstrait avec timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class BaseModel(TimeStampedModel):
    """Modèle de base avec ID ObjectId"""
    id = ObjectIdField(primary_key=True)
    
    class Meta:
        abstract = True