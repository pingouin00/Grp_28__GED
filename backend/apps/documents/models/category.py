from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField
from apps.common.models import TimeStampedModel

class Category(TimeStampedModel):
    id = ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['created_by', 'name']),
        ]
    
    def __str__(self):
        return self.name