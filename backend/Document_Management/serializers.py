from django.contrib.auth.models import User
from rest_framework import serializers
from bson import ObjectId 
from .models import Note ,Document, Category, Tag, DocumentVersion, DocumentShare
import re

import magic 

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return ObjectId(data)

class UserSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True}
        } # tell django don't let the password be read  when you give the user data 
     
    def validate_password(self, value):
        strength = self.check_password_strength(value)
        if strength == "faible":
            raise serializers.ValidationError(
                "Le mot de passe est trop faible. Il doit comporter au moins 8 caractères, une majuscule, une minuscule et un caractère spécial pour être considéré comme fort."
            )
        return value
    
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user
    
    def check_password_strength(self, password):
        """Retourne 'faible', 'moyen' ou 'fort' selon la complexité du mot de passe."""
        length = len(password) >= 8
        has_upper = re.search(r"[A-Z]", password)
        has_lower = re.search(r"[a-z]", password)
        has_digit = re.search(r"\d", password)
        has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

        if length and has_upper and has_lower and has_special:
            return "fort"
        elif length and ((has_upper and has_lower) or (has_digit and has_special)):
            return "moyen"
        else:
            return "faible"

# Serializer pour afficher le profil utilisateur
class UserProfileSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    date_joined = serializers.DateTimeField(format="%d %B %Y %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]

# Serializer pour modifier le profil utilisateur
class UserUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["username", "new_password", "confirm_new_password"]

    def validate(self, data):
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_new_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
            if len(new_password) < 8:
                raise serializers.ValidationError("Le nouveau mot de passe doit comporter au moins 8 caractères.")
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        new_password = validated_data.get("new_password")

        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance
  
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}} # opposite for the userserialiser , backend decides 
        
class CategorySerializer(serializers.ModelSerializer):
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'created_by', 'document_count']
        extra_kwargs = {"created_by": {"read_only": True}}
    
    def get_document_count(self, obj):
        return obj.documents.count()
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
class DocumentListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file_type', 'file_size', 
                 'created_at', 'updated_at', 'owner_username', 'category_name', 
                 'tags', 'is_public']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
        
class DocumentDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=Tag.objects.all(),
        required=False
    )
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file', 'file_type', 'file_size', 
                 'created_at', 'updated_at', 'owner', 'owner_username', 'category', 
                 'category_name', 'tags', 'tag_ids', 'is_public']
        extra_kwargs = {
            "owner": {"read_only": True},
            "file_type": {"read_only": True},
            "file_size": {"read_only": True},
        }
    
    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        document = Document.objects.create(**validated_data)
        
        # Détecter le type MIME du fichier
        if document.file:
            mime = magic.Magic(mime=True)
            document.file_type = mime.from_file(document.file.path)
            document.save()
        
        # Ajouter les tags
        document.tags.set(tag_ids)
        
        # Créer une première version du document
        if document.file:
            DocumentVersion.objects.create(
                document=document,
                file=document.file,
                version_number=1,
                created_by=document.owner,
                comments="Version initiale"
            )
        return document
    
    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Mise à jour des champs de base
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        # Si un nouveau fichier est téléchargé, créer une nouvelle version
        if 'file' in validated_data:
            # Détecter le type MIME du fichier
            mime = magic.Magic(mime=True)
            instance.file_type = mime.from_file(instance.file.path)
            
            # Créer une nouvelle version
            latest_version = instance.versions.order_by('-version_number').first()
            version_number = 1 if not latest_version else latest_version.version_number + 1
            
            DocumentVersion.objects.create(
                document=instance,
                file=instance.file,
                version_number=version_number,
                created_by=self.context['request'].user,
                comments=f"Version {version_number}"
            )
        instance.save()
        # Mettre à jour les tags si fournis
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance
    
class DocumentVersionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = DocumentVersion
        fields = ['id', 'document', 'file', 'version_number', 'created_at', 
                 'created_by', 'created_by_username', 'comments']
        extra_kwargs = {
            "document": {"read_only": True},
            "created_by": {"read_only": True},
            "version_number": {"read_only": True},
        }

class DocumentShareSerializer(serializers.ModelSerializer):
    shared_with_username = serializers.ReadOnlyField(source='shared_with.username')
    document_title = serializers.ReadOnlyField(source='document.title')
    
    class Meta:
        model = DocumentShare
        fields = ['id', 'document', 'document_title', 'shared_with', 
                 'shared_with_username', 'created_at', 'can_edit']
        extra_kwargs = {
            "created_at": {"read_only": True},
        }
    
    def validate(self, data):
        # Vérifier que l'utilisateur ne partage pas le document avec lui-même
        if data['shared_with'] == self.context['request'].user:
            raise serializers.ValidationError("Vous ne pouvez pas partager un document avec vous-même.")
        
        # Vérifier que l'utilisateur est propriétaire du document
        if data['document'].owner != self.context['request'].user:
            raise serializers.ValidationError("Vous ne pouvez partager que vos propres documents.")
        
        return data