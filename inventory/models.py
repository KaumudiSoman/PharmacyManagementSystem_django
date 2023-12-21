from django.db import models

# Create your models here.
class Inventory(models.Model):
    inventory_id = models.CharField(unique=True, max_length=100)
    quantity = models.IntegerField()
    expiry_date = models.DateField()
    batch_no = models.CharField(max_length=100)
    medicine_id = models.ForeignKey('Medicine', null=False, blank=False, on_delete=models.CASCADE)
    branch = models.ForeignKey('branch.Branch', null=False, blank=False, on_delete=models.CASCADE)


class Medicine(models.Model):
    medicine_id = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=100)
    price = models.FloatField()
