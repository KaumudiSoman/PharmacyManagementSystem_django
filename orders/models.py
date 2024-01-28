from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Max
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser
from branch.models import Branch 
import uuid
from django.utils import timezone
from inventory.models import Medicine
# Create your models here.


class Orders(models.Model):
    PURCHASE = 'purchase'
    SALES = 'sales'
    ORDER_CHOICES = [(PURCHASE, 'purchase'), (SALES, 'sales'),]

    order_id = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)
    order_date = models.DateField()
    total = models.IntegerField(null=True, blank=True)
    type = models.CharField(choices=ORDER_CHOICES, max_length=20)

    order_from_type = models.ForeignKey(ContentType, on_delete = models.CASCADE, null = True, blank = True, related_name='order_from_content_type')
    order_from_id = models.CharField(null=True, blank=True, max_length = 100)
    order_from = GenericForeignKey('order_from_type', 'order_from_id')

    order_to_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, related_name='order_to_content_type')
    order_to_id = models.CharField(null=True, blank=True, max_length = 100)
    order_to = GenericForeignKey('order_to_type', 'order_to_id')

    def update_total(self):
        try:
            total = MedicineLines.objects.filter(order_id=self).aggregate(Sum('line_total'))['line_total__sum']
            self.total = total or 0
            self.save()
        except Exception as e:
            print(f'Can not save order total : {e}')

    def set_order_date(self):
        self.order_date = timezone.now().date()

    def save(self, *args, **kwargs):
        if self.type == self.SALES:
            try:
                self.order_from_type = ContentType.objects.get_for_model(CustomUser)
                self.order_to_type = ContentType.objects.get_for_model(Branch)
            except ContentType.DoesNotExist:
                raise ValueError("Content type does not exist for CustomUser or Branch.")
            
        elif self.type == self.PURCHASE:
            try:
                self.order_from_type = ContentType.objects.get_for_model(Branch)
                self.order_to_type = ContentType.objects.get_for_model(CustomUser)
            except ContentType.DoesNotExist:
                raise ValueError("Content type does not exist for CustomUser or Branch.")

        self.set_order_date()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.order_id)


class MedicineLines(models.Model):
    line_no = models.IntegerField(unique=True)
    price = models.FloatField()
    line_total = models.FloatField()
    quantity = models.IntegerField()
    order = models.ForeignKey('orders.Orders', on_delete=models.CASCADE, default=0)
    medicine_id = models.ForeignKey('inventory.Medicine', on_delete=models.CASCADE, default=0)

    class Meta:
        unique_together = ('order', 'medicine_id')

    def save(self, *args, **kwargs):
        if not self.pk:
            max_line_no = MedicineLines.objects.filter(order=self.order).aggregate(Max('line_no'))['line_no__max']
            if max_line_no:
                self.line_no = max_line_no + 1
            else:
                self.line_no = 1

        if self.medicine_id:
            medicine_price = Medicine.objects.get(medicine_id=self.medicine_id)
            self.price = medicine_price

        self.line_total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.line_no


@receiver(post_save, sender=MedicineLines)
def update_order_total(sender, instance, **kwargs):
    if instance.order:
        instance.order.update_total()






    # order_to_customer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='customer_orders', null=True, blank=True)
    # order_to_branch = models.ForeignKey('branch.Branch', on_delete=models.CASCADE, related_name='branch_orders', null=True, blank=True)

    # order_to = models.ForeignKey('branch.branch' if order_from == CUSTOMER else 'accounts.CustomUser')
    # customer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='customer_orders', null=True, blank=True)
    # vendor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='vendor_orders', null=True, blank=True)
    # employee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='employee_orders', null=True, blank=True)
    # branch = models.ForeignKey('branch.Branch', on_delete=models.CASCADE)
        
    
    # CUSTOMER = 'customer'
    # BRANCH = 'branch'
    # ORDER_FROM_CHOICES = [(CUSTOMER, 'customer'), (BRANCH, 'branch')]