from rest_framework import permissions
from reviews.models import User

superuser = User.objects.filter(role='superuser')
admin = User.objects.filter(role='admin')


class IsAuthorModeratorOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        moderator = User.objects.filter(role='moderator')
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or obj.author == moderator


class IsSuperuserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == admin or obj.author == superuser
