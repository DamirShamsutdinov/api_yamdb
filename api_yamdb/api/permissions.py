
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

from reviews.models import User

MODERATOR = User.objects.filter(role='moderator')


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or obj.author == MODERATOR


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or (obj.author == request.user
                or request.user.is_superuser
                or request.user.is_moderator))

class IsNotAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_anonymous