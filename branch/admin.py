from django.contrib import admin
from .models import Branch, CustomUserBranchRelation

# Register your models here.

class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch_id', 'name', 'phno', 'address']

class CustomUserBranchRelationAdmin(admin.ModelAdmin):
    list_display = ['user', 'branch', 'get_user_role']

    def get_user_role(self, obj):
        return obj.user.role

    # def display_user_role(self, obj):
    #     return obj.user_role

    # display_user_role.short_description = 'User Role'

admin.site.register(Branch, BranchAdmin)
admin.site.register(CustomUserBranchRelation, CustomUserBranchRelationAdmin)

