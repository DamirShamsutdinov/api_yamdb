from rest_framework import permissions

from users.models import ADMIN, MODERATOR


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.role == MODERATOR
            or request.user.is_superuser
            or request.user.role == ADMIN
        )


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.role == ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.role == ADMIN
        )


class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or (obj.author == request.user
                    or request.user.role == MODERATOR
                    or request.user.role == ADMIN))


class IsAdminOrSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == ADMIN or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.role == ADMIN:
            return True
        return False
