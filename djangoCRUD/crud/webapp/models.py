from django.contrib.auth.models import User
from django.db import models


class Branch(models.Model):
    branch_code = models.CharField(max_length=50, unique=True)
    branch_name = models.CharField(max_length=100)
    branch_type = models.CharField(max_length=100)  # e.g., Retail, Corporate, etc.

    def __str__(self):
        return f"{self.branch_code} - {self.branch_name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('cashier', 'Cashier')])
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='profiles')  # Profile is linked to a branch

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"




class Record(models.Model):
    category_id = models.CharField(max_length=50)
    category_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.category_id + " " + self.category_desc


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_fullname = models.CharField(max_length=255, blank=True)
    customer_firstname = models.CharField(max_length=255, blank=True)
    customer_middlename = models.CharField(max_length=255, blank=True, null=True)
    customer_lastname = models.CharField(max_length=255, blank=True)
    customer_address = models.CharField(max_length=255, blank=True)
    customer_level = models.CharField(default='---', max_length=1, choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ])

    def __str__(self):
        return self.customer_fullname
    


class BICSetup(models.Model):
    product_code = models.AutoField(primary_key=True)
    category = models.ForeignKey(Record, on_delete=models.CASCADE)
    item_code = models.CharField(max_length=100, blank=True)
    product_desc = models.CharField(max_length=100, blank=True)
    product_barcode = models.CharField(max_length=100, blank=True)
    level_1 = models.FloatField(default=None, blank=True)
    level_2 = models.FloatField(default=None, blank=True)
    level_3 = models.FloatField(default=None, blank=True)
    level_4 = models.FloatField(default=None, blank=True)
    level_5 = models.FloatField(default=None, blank=True)
    unit = models.CharField(max_length=100, blank=True)
    product_price = models.IntegerField() 

    def __str__(self):
        return self.product_code + " " + self.product_desc







class MCRegister(models.Model):
    branch_name = models.CharField(max_length=50, default='')  
    date_issued = models.CharField(max_length=100, default='')
    payee = models.CharField(max_length=50, default='')
    amount = models.IntegerField(default='')  
    check_number = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='')
    branch_remarks = models.TextField(default='') 

    def __str__(self):
        return f"{self.branch_name} ({self.date_issued})"
    


class PesoNet(models.Model):
    branch_name = models.CharField(max_length=100, default='')  
    OFI_reference_num = models.IntegerField( default='')
    transact_amount = models.IntegerField( default='')
    transact_date = models.CharField(max_length=100, default='')  
    status = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.branch_name} ({self.OFI_reference_num})"     

