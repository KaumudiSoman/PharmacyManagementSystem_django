from rest_framework.permissions import BasePermission
from .models import CustomUser

# For all employees
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        employee_roles = [
            CustomUser.SEMPLOYEE,
            CustomUser.CEMPLOYEE,
            CustomUser.MEMPLOYEE,
            CustomUser.AEMPLOYEE
        ]
        return (request.user.role in employee_roles and request.user.is_verified)
    

# For cashiers and above
class IsCashierX(BasePermission):
    def has_permission(self, request, view):
        employee_roles = [
            CustomUser.CEMPLOYEE,
            CustomUser.MEMPLOYEE,
            CustomUser.AEMPLOYEE
        ]
        return (request.user.role in employee_roles and request.user.is_verified)
    

# For Managers and above
class IsManagerX(BasePermission):
    def has_permission(self, request, view):
        employee_roles = [
            CustomUser.MEMPLOYEE,
            CustomUser.AEMPLOYEE
        ]
        return (request.user.role in employee_roles and request.user.is_verified)
    


# For administrators
class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == CustomUser.AEMPLOYEE and request.user.is_verified)