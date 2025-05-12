from rest_framework import permissions

# class IsAdminUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Les méthodes de lecture sont toujours autorisées
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Vérifier si l'objet a un attribut 'owner' ou 'author' ou 'created_by'
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
            
        return False
    
class IsOwnerOrSharedWith(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Vérifier si l'utilisateur est le propriétaire
        if hasattr(obj, 'owner') and obj.owner == user:
            return True
            
        # Vérifier si le document est public
        if hasattr(obj, 'is_public') and obj.is_public:
            return request.method in permissions.SAFE_METHODS
            
        # Vérifier si le document est partagé avec l'utilisateur
        if hasattr(obj, 'shares'):
            # Pour les méthodes de modification, vérifier le droit d'édition
            if request.method in permissions.SAFE_METHODS:
                return obj.shares.filter(shared_with=user).exists()
            else:
                return obj.shares.filter(shared_with=user, can_edit=True).exists()
                
        return False