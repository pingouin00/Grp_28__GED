from rest_framework import serializers
from ..models import Document, Category, Tag
from .category import CategorySerializer
from .tag import TagSerializer
from apps.common.serializers import ObjectIdField
from apps.documents.utils.validators import validate_file_extension, validate_file_size, validate_file_type

class DocumentListSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    file_size_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'original_filename', 'file_type',
            'file_size', 'file_size_formatted', 'is_public', 'download_count',
            'created_at', 'updated_at', 'owner', 'category', 'tags'
        ]
    
    def get_file_size_formatted(self, obj):
        from apps.common.utils import format_file_size
        return format_file_size(obj.file_size)

class DocumentDetailSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    category_id = ObjectIdField(write_only=True, required=False, allow_null=True)
    category = CategorySerializer(read_only=True)
    tag_ids = ObjectIdField(many=True, write_only=True, required=False)
    tags = TagSerializer(many=True, read_only=True)
    file = serializers.FileField(write_only=True, required=False)
    file_size_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'original_filename', 'file_type',
            'file_size', 'file_size_formatted', 'is_public', 'download_count',
            'created_at', 'updated_at', 'owner', 'category', 'category_id',
            'tags', 'tag_ids', 'file'
        ]
        read_only_fields = ['owner', 'original_filename', 'file_type', 'file_size']
    
    def get_file_size_formatted(self, obj):
        from apps.common.utils import format_file_size
        return format_file_size(obj.file_size)
    
    def validate_file(self, value):
        validate_file_extension(value)
        validate_file_size(value)
        validate_file_type(value)
        return value
    
    def validate_category_id(self, value):
        if value and not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("Catégorie invalide")
        return value
    
    def validate_tag_ids(self, value):
        if value:
            existing_tags = Tag.objects.filter(id__in=value)
            if len(existing_tags) != len(value):
                raise serializers.ValidationError("Un ou plusieurs tags sont invalides")
        return value
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        file_obj = validated_data.pop('file', None)
        
        if category_id:
            validated_data['category'] = Category.objects.get(id=category_id)
        
        document = Document.objects.create(**validated_data)
        
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            document.tags.set(tags)
        
        if file_obj:
            document.save_file_to_gridfs(file_obj)
            document.save()
        
        return document
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', None)
        file_obj = validated_data.pop('file', None)
        
        if category_id is not None:
            instance.category = Category.objects.get(id=category_id) if category_id else None
        
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids) if tag_ids else []
            instance.tags.set(tags)
        
        if file_obj:
            instance.delete_file_from_gridfs()
            instance.save_file_to_gridfs(file_obj)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance