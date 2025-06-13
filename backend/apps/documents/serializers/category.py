from rest_framework import serializers
from ..models import Category
from apps.common.serializers import ObjectIdField

class CategorySerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'created_by']