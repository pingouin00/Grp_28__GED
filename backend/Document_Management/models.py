from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField

class Note(models.Model):
    id = ObjectIdField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")#to indicate that we will be linking to a data source(user) , and gives the option that if we want to delete the user we also delete all the notes the user has 

    def __str__(self):
        return self.title