from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        employee_roles = [
            CustomUser.SEMPLOYEE,
            CustomUser.CEMPLOYEE,
            CustomUser.MEMPLOYEE,
            CustomUser.AEMPLOYEE
        ]
        return request.user.role in employee_roles