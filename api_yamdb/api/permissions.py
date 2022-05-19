from rest_framework import permissions
from users.models import User


# Reviews, Comment,
class IsModeratorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.ADMIN
            or request.user.is_superuser
            or request.user.role == User.MODERATOR
        )


# Genre, Categories, Title
class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.role == User.ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.role == User.ADMIN
        )


class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.MODERATOR
            or request.user.role == User.ADMIN
        )


# User
class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.ADMIN or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == User.ADMIN
