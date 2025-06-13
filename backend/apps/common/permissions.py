from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission pour les propriétaires avec lecture pour tous"""
    
    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissions d'écriture seulement pour le propriétaire
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False

class IsOwnerOrSharedWith(permissions.BasePermission):
    """Permission pour propriétaires et utilisateurs partagés"""
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Propriétaire a tous les droits
        if hasattr(obj, 'owner') and obj.owner == user:
            return True
        
        # Documents publics en lecture seule
        if hasattr(obj, 'is_public') and obj.is_public:
            return request.method in permissions.SAFE_METHODS
        
        # Vérifier les partages
        if hasattr(obj, 'shares'):
            if request.method in permissions.SAFE_METHODS:
                return obj.shares.filter(shared_with=user).exists()
            else:
                return obj.shares.filter(shared_with=user, can_edit=True).exists()
        
        return False