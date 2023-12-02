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

admin.site.register(CustomUser)
# admin.site.register(Branch)
# admin.site.register(Orders)
# admin.site.register(Users, VendorAdmin)
# admin.site.register(Users, CustomerAdmin)
# admin.site.register(Users, EmployeeAdmin)