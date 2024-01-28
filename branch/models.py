from django.db import models
# from accounts.models import CustomUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import uuid

# Create your models here.

class Branch(models.Model):
    branch_id = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=500)
    phno = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class CustomUserBranchRelation(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=False, blank=False)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=False, blank=False)
    # is_employee = models.BooleanField(default=False)

    # employee_roles = ['employee-cashier', 'employee-salesman', 'employee-manager', 'employee-administrator']
    # is_employee__in = employee_roles

    class Meta:
        unique_together = ('user', 'branch')

    def __str__(self):
        return self.user.email


@receiver(pre_save, sender=CustomUserBranchRelation)
def enforce_employee_constraine(sender, instance, **kwargs):
    # is_employee = instance.is_employee
    user_role = instance.user.role
    # def user_role(self):
    #     return self.user.role
    
    existing_employee = CustomUserBranchRelation.objects.filter(user=instance.user).exists()

    if user_role.startswith('employee-') and existing_employee:
        raise ValidationError('The employee is already associated with a branch')
    
