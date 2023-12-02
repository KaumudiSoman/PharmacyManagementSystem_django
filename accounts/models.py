from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from branch.models import Branch, CustomUserBranchRelation
# from orders.models import Orders

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError('User must enter email')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **other_fields)
    

class CustomUser(AbstractBaseUser):
    EMPLOYEE = 'employee'
    VENDOR = 'vendor'
    CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    ]
    user_id = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    address = models.TextField(max_length=500)
    role = models.CharField(null=False, blank=False, max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def _get_relations_by_role(self, is_employee):
            return CustomUserBranchRelation.objects.filter(user=self, is_employee=is_employee)

    @property
    def is_customer(self):
        return self.role == 'customer'

    @property
    def is_employee(self):
        return self.role == 'employee'

    @property
    def branches(self):
        if self.is_employee:
            return Branch.objects.filter(userbranchrelation__in=self._get_relations_by_role(is_employee=True))
        elif self.is_customer:
            return Branch.objects.filter(userbranchrelation__in=self._get_relations_by_role(is_employee=False))
        else:
            return Branch.objects.none()
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# class UserBranchRelation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     is_employee = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('user', 'branch')


# class Users(models.Model):
#     EMPLOYEE = 'employee'
#     VENDOR = 'vendor'
#     CUSTOMER = 'customer'

#     ROLE_CHOICES = [
#         (EMPLOYEE, 'Employee'),
#         (VENDOR, 'Vendor'),
#         (CUSTOMER, 'Customer'),
#     ]
#     user_id = models.IntegerField(unique=True)
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     dob = models.DateField()
#     address = models.TextField(max_length=500)
#     role = models.CharField(null=False, blank=False, max_length=10, choices=ROLE_CHOICES)
#     branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     order_id = models.ForeignKey(PurchaseOrder, on_delete=models.DO_NOTHING)