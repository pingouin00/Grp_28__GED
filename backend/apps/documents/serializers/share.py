from rest_framework import serializers
from django.contrib.auth.models import User
from apps.documents.models import DocumentShare
from apps.common.serializers import ObjectIdField

class DocumentShareSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    document = serializers.StringRelatedField(read_only=True)
    shared_with = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    shared_with_email = serializers.EmailField(
        source='shared_with.email', 
        read_only=True
    )
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentShare
        fields = [
            'id', 'document', 'shared_with', 'shared_with_email',
            'can_edit', 'expires_at', 'created_at', 'is_expired'
        ]
    
    def get_is_expired(self, obj):
        return obj.is_expired()
    
    def validate_shared_with(self, value):
        """Empêcher de partager avec soi-même"""
        request = self.context.get('request')
        if request and request.user == value:
            raise serializers.ValidationError(
                "Vous ne pouvez pas partager un document avec vous-même"
            )
        return value
    
    def validate(self, data):
        """Validation des données de partage"""
        document = self.context.get('document')
        shared_with = data.get('shared_with')
        
        if document and shared_with:
            # Vérifier si le partage existe déjà
            existing_share = DocumentShare.objects.filter(
                document=document,
                shared_with=shared_with
            ).first()
            
            if existing_share and not self.instance:
                raise serializers.ValidationError(
                    "Ce document est déjà partagé avec cet utilisateur"
                )
        
        return data