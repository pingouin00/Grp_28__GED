from rest_framework import serializers
from bson import ObjectId, errors as bson_errors

class ObjectIdField(serializers.Field):
    """Champ personnalisé pour ObjectId MongoDB"""
    
    def to_representation(self, value):
        if value is None:
            return None
        return str(value)
    
    def to_internal_value(self, data):
        if data is None:
            return None
        try:
            return ObjectId(data)
        except (bson_errors.InvalidId, TypeError, ValueError):
            raise serializers.ValidationError("Invalid ObjectId format")