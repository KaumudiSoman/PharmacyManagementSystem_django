from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

# Create your models here.
class Inventory(models.Model):
    inventory_id = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)
    quantity = models.IntegerField()
    expiry_date = models.DateField()
    batch_no = models.CharField(max_length=100)
    medicine_id = models.ForeignKey('Medicine', null=False, blank=False, on_delete=models.CASCADE)
    branch = models.ForeignKey('branch.Branch', null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('medicine_id', 'branch')

    def __str__(self):
        return str(self.inventory_id)
    
# Sends email to the manager if quantity of any medicine goes below 50
@receiver(post_save, sender=Inventory)
def check_inventory(sender, instance, created, **kwargs):
    if instance.quantity <= 50:
        subject = 'Low Inventory Alert'
        message = f'Quantity for medicine {instance.medicine_id} is {instance.quantity}. Please place order.'
        manager_email = 'kaumudisoman123@gmail.com'
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, [manager_email])
        print('Email sent sucessfully')



class Medicine(models.Model):
    medicine_id = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return str(self.medicine_id)