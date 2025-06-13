from rest_framework import permissions

class IsOwnerProfile(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser seulement le propriétaire du profil.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAccountOwner(permissions.BasePermission):
    """
    Permission pour autoriser seulement le propriétaire du compte.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user