from django.contrib import admin
from .models import Orders, MedicineLines

# Register your models here.

class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'type', 'total', 'order_from_id', 'order_to_id', 'order_date']

class SalesMedicineLinesAdmin(admin.ModelAdmin):
    list_display = ['line_no', 'medicine_id', 'order', 'price', 'quantity', 'line_total']

admin.site.register(Orders, SalesOrderAdmin)
admin.site.register(MedicineLines, SalesMedicineLinesAdmin)
