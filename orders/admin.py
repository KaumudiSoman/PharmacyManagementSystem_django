from django.contrib import admin
from .models import Orders, MedicineLines

# Register your models here.
admin.site.register(Orders)
admin.site.register(MedicineLines)
