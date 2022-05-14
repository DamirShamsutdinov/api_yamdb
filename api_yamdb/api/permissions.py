from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from reviews.models import User

MODERATOR = User.objects.filter(role='moderator')


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or obj.author == MODERATOR


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)

class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or (obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator))