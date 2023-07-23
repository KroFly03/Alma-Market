from rest_framework.permissions import BasePermission

from users.models import User


class AdminRequired(BasePermission):
    message = 'Необходимо быть администратором, чтобы выполнить данное действие.'

    def has_permission(self, request, view):
        if request.user.role == User.Roles.ADMIN:
            return True
