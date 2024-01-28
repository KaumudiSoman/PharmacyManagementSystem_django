from django.db import models
import uuid

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


class Medicine(models.Model):
    medicine_id = models.UUIDField(default=uuid.uuid4, auto_created=True, primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return str(self.medicine_id)