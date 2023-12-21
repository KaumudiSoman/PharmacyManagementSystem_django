from django.db import models
# from accounts.models import CustomUser
# from branch.models import Branch

# Create your models here.


class Orders(models.Model):
    PURCHASE = 'purchase'
    SALES = 'sales'
    ORDER_CHOICES = [(PURCHASE, 'purchase'), (SALES, 'sales'),]
    order_id = models.CharField(unique=True, max_length=100)
    order_date = models.DateField()
    total = models.IntegerField()
    type = models.CharField(choices=ORDER_CHOICES, max_length=10)
    customer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='customer_orders', null=True, blank=True)
    vendor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='vendor_orders', null=True, blank=True)
    employee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='employee_orders', null=True, blank=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id


class MedicineLines(models.Model):
    line_no = models.IntegerField(unique=True)
    price = models.FloatField()
    line_total = models.IntegerField()
    quantity = models.IntegerField()
    order_id = models.ForeignKey('orders.Orders', on_delete=models.CASCADE, null=True, blank=True)
    medicine_id = models.ForeignKey('inventory.Medicine', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.line_total = self.price * self.quantity
        super().save(*args, **kwargs)