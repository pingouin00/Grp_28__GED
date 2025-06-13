import re 
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField
from apps.common.models import TimeStampedModel

class UserProfile(TimeStampedModel):
    id = ObjectIdField(primary_key=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"Profile de {self.user.username}"