from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from apps.common.serializers import ObjectIdField
import re

class UserSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True}
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cette adresse email est déjà utilisée.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return value
    
    def validate_password(self, value):
        if not self._is_password_strong(value):
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule, un chiffre et un caractère spécial."
            )
        return value
    
    def _is_password_strong(self, password):
        """Vérifie la force du mot de passe."""
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', format="%d/%m/%Y", read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'avatar', 'bio', 'phone', 'address', 'date_of_birth',
            'date_joined', 'is_email_verified'
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'bio', 'phone', 
            'address', 'date_of_birth', 'current_password', 
            'new_password', 'confirm_password'
        ]
    
    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        current_password = data.get('current_password')
        
        if new_password or confirm_password:
            if not current_password:
                raise serializers.ValidationError("Mot de passe actuel requis.")
            if new_password != confirm_password:
                raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
            if not self._is_password_strong(new_password):
                raise serializers.ValidationError(
                    "Le nouveau mot de passe doit contenir au moins 8 caractères, "
                    "une majuscule, une minuscule, un chiffre et un caractère spécial."
                )
        
        return data
    
    def _is_password_strong(self, password):
        return len(password) >= 8 and re.search(r"[A-Z]", password) and \
               re.search(r"[a-z]", password) and re.search(r"\d", password) and \
               re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    
    def update(self, instance, validated_data):
        user_data = {}
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
        
        current_password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('confirm_password', None)
        
        # Mise à jour du profil
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Mise à jour de l'utilisateur
        user = instance.user
        if current_password and new_password:
            if not user.check_password(current_password):
                raise serializers.ValidationError("Mot de passe actuel incorrect.")
            user.set_password(new_password)
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        
        user.save()
        instance.save()
        return instance