from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsOwnerOrReadOnly(BasePermission):
    """Custom permission class to allow only bookmark owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the bookmark owner."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
