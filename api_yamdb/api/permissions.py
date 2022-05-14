from rest_framework import permissions

from reviews.models import User

MODERATOR = User.objects.filter(role='moderator')


class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or obj.author == MODERATOR or request.user.is_superuser


class IsAdminUserOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


# class IsUserAdminModeratorOrReadOnly(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated)
#
#     def has_object_permission(self, request, view, obj):
#         return ((request.method in permissions.SAFE_METHODS)
#                 or (obj.author == request.user
#                 or request.user.is_superuser
#                 or request.user.is_moderator))

