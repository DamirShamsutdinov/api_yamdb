from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, IsAdminUser
from reviews.models import User

MODERATOR = User.objects.filter(role='moderator')


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or obj.author == MODERATOR
        # return obj.author == request.user or self.user.is_MODERATOR


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
