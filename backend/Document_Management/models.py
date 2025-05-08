from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField
import os

class Note(models.Model):
    id = ObjectIdField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")#to indicate that we will be linking to a data source(user) , and gives the option that if we want to delete the user we also delete all the notes the user has 

    def __str__(self):
        return self.title
    
class Category(models.Model):
    id = ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories") 

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    id = ObjectIdField(primary_key=True)
    name = models.CharField(max_length=50 , unique=True)

    def __str__(self):
        return self.name
    
def document_file_path(instance, filename):
    # Génère le chemin pour les fichiers uploadés
    ext = filename.split('.')[-1]
    filename = f"{instance.title.replace(' ', '_')}_{instance.id}.{ext}"
    return os.path.join('documents', str(instance.owner.id), filename)

class Document(models.Model):
    id = ObjectIdField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    file = models.FileField(upload_to=document_file_path)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)  # en octets
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents") 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="documents", null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="documents", blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Mettre à jour le type et la taille du fichier à l'enregistrement
        if self.file:
            self.file_size = self.file.size
            # Le type est géré dans le sérialiseur avec python-magic
        super().save(*args, **kwargs)

class DocumentVersion(models.Model):
    id = ObjectIdField(primary_key=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="versions") 
    
    file = models.FileField(upload_to=document_file_path)
    version_number = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="document_versions")
    
    comments = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['document', 'version_number']
        ordering = ['-version_number']
    
    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"
    
class DocumentShare(models.Model):
    id = ObjectIdField(primary_key=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="shares")
    
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_documents")
    created_at = models.DateTimeField(auto_now_add=True)
    can_edit = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['document', 'shared_with']
    
    def __str__(self):
        return f"{self.document.title} partagé avec {self.shared_with.username}"

    