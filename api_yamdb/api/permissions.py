from rest_framework import permissions
from reviews.models import User

MODERATOR = User.objects.filter(role='moderator')

class IsModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if self.request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or obj.author == MODERATOR


# class IsAuthorOrAdminPermission(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.method == "GET" or request.method == "PATCH":
#             return obj.author == request.user or obj.author == MODERATOR or self.request.user.is_superuser
#         return False
