from django.contrib import admin
# from branch.models import Branch
# from orders.models import Orders
from .models import CustomUser

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'email', 'phno', 'address']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'email', 'phno', 'branch_id']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'email', 'phno', 'branch_id']

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'is_staff', 'is_admin', 'is_superuser', 'is_verified'] 

admin.site.register(CustomUser, UserAdmin)
# admin.site.register(Branch)
# admin.site.register(Orders)
# admin.site.register(Users, VendorAdmin)
# admin.site.register(Users, CustomerAdmin)
# admin.site.register(Users, EmployeeAdmin)