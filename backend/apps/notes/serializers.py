from rest_framework import serializers
from .models import Note
from apps.common.serializers import ObjectIdField

class NoteListSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'created_at', 'updated_at', 'author']

class NoteDetailSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author']
        read_only_fields = ['author']

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'content']
        extra_kwargs = {
            'content': {'required': True}
        }

class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'content']
        extra_kwargs = {
            'title': {'required': False},
            'content': {'required': False}
        }