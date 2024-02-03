from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Max
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser
from branch.models import Branch 
import uuid
from django.utils import timezone
# Create your models here.


# Sales order is from CustomUser(Customer) to Branch
# Purchase order is from Branch to CustomUser(Vendor)
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

    # Calcualetes total price according to medicine lines
    def update_total(self):
        try:
            total = MedicineLines.objects.filter(order_id=self).aggregate(Sum('line_total'))['line_total__sum']
            self.total = total or 0
            self.save()
        except Exception as e:
            print(f'Can not save order total : {e}')

    # Sets order date to current date
    def set_order_date(self):
        self.order_date = timezone.now().date()

    # Specifies order_to and order_from fields according to order type
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
    line_no = models.IntegerField()
    price = models.FloatField()
    line_total = models.FloatField()
    quantity = models.IntegerField()
    order = models.ForeignKey('orders.Orders', on_delete=models.CASCADE, default=0)
    medicine_id = models.ForeignKey('inventory.Medicine', on_delete=models.CASCADE, default=0)

    class Meta:
        unique_together = ('order', 'medicine_id')

    def save(self, *args, **kwargs):
        # Gives unique line number to each medicine line for each order
        if not self.pk:
            max_line_no = MedicineLines.objects.filter(order=self.order).aggregate(Max('line_no'))['line_no__max']
            if max_line_no:
                self.line_no = max_line_no + 1
            else:
                self.line_no = 1

        # Sets price as the price of medicine in Medicine model
        if self.medicine_id:
            self.price = self.medicine_id.price

        # Calculates line total for each medicine line
        self.line_total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.line_no


# Updates total price of order post save medicine lines
@receiver(post_save, sender=MedicineLines)
def update_order_total(sender, instance, **kwargs):
    if instance.order:
        instance.order.update_total()