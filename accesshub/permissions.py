# accesshub/permissions.py

from rest_framework.permissions import BasePermission

class IsActiveUser(BasePermission):
    message = "User account is not activated."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )

