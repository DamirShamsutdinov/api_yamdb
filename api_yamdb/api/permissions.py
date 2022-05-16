from rest_framework import permissions

MODERATOR = 'moderator'


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.role == MODERATOR
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or (obj.author == request.user
                    or request.user.role == MODERATOR
                    or request.user.is_superuser))


class IsAdminOrAnonymousUser(permissions.IsAdminUser):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or not request.user.is_authenticated:
            return True
        return False
