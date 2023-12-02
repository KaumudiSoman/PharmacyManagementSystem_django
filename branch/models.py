from django.db import models
# from accounts.models import CustomUser

# Create your models here.


class Branch(models.Model):
    branch_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=500)
    phno = models.CharField(max_length=10)
    user_relation = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=False, blank=False, related_name='user_branch_relations')
    # employee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=False, blank=False, related_name='employee_works')
    # customer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=False, blank=False, related_name='customer_goes')

    def __str__(self):
        return self.branch_id
    

class CustomUserBranchRelation(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    is_employee = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'branch')
