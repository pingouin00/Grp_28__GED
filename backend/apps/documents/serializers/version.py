from rest_framework import serializers
from apps.documents.models import DocumentVersion
from apps.common.serializers import ObjectIdField
from apps.common.utils import format_file_size

class DocumentVersionSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    document = serializers.StringRelatedField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    file_size_formatted = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True)
    
    class Meta:
        model = DocumentVersion
        fields = [
            'id', 'document', 'version_number', 'created_by',
            'comments', 'file_size', 'file_size_formatted',
            'file_hash', 'created_at', 'file'
        ]
        read_only_fields = [
            'version_number', 'created_by', 'file_size', 'file_hash'
        ]
    
    def get_file_size_formatted(self, obj):
        return format_file_size(obj.file_size)
    
    def validate_file(self, value):
        """Validation du fichier de version"""
        from apps.documents.utils.validators import (
            validate_file_extension, 
            validate_file_size, 
            validate_file_type
        )
        
        validate_file_extension(value)
        validate_file_size(value)
        validate_file_type(value)
        
        return value
    
    def create(self, validated_data):
        file_obj = validated_data.pop('file', None)
        version = super().create(validated_data)
        
        if file_obj:
            version.save_version_to_gridfs(file_obj)
            version.save()
        
        return version