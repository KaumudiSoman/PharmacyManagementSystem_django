from django.contrib import admin
from .models import Inventory, Medicine

# Register your models here.

class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_id', 'name', 'price']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['inventory_id', 'quantity', 'batch_no', 'medicine_id', 'branch']

admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Medicine, MedicineAdmin)
