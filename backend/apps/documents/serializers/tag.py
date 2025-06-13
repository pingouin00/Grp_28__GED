from rest_framework import serializers
from ..models import Tag
from apps.common.serializers import ObjectIdField

class TagSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']