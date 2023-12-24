from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from branch.models import Branch, CustomUserBranchRelation

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('User must enter email')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_verified',True)
        self.is_staff = True
        self.is_superuser=True
        self.set_password=password

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **other_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    CEMPLOYEE = 'employee-cashier'
    SEMPLOYEE = 'employee-salesman'
    MEMPLOYEE = 'employee-manager'
    AEMPLOYEE = 'employee-administrator'
    VENDOR = 'vendor'
    CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (CEMPLOYEE, 'Employee-Cashier'),
        (SEMPLOYEE, 'Employee-Salesman'),
        (MEMPLOYEE, 'Employee-Manager'),
        (AEMPLOYEE, 'employee-Administrator'),
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    ]
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True)
    address = models.TextField(max_length=500)
    role = models.CharField(null=False, blank=False, max_length=30, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


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