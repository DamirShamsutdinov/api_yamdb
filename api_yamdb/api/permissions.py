from rest_framework import permissions
from reviews.models import User

MODERATOR = User.objects.filter(role='moderator')


class IsContentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.request.user.is_admin or self.request.user.is_superuser


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or self.request.is_MODERATOR or self.request.user.is_admin or self.request.user.is_superuser

