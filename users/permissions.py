from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def is_allowed_action(self, request, view):
        if view.action == 'list':
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user