from django.db import models
from django.core import validators
from datetime import date

class employee(models.Model):
    name = models.CharField(max_length=100)
    employee_code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.employee_code


class vendor(models.Model):
    name = models.CharField(max_length=100)
    vendor_code = models.CharField(max_length=100)
    
    def __str__(self):
        return self.vendor_code

class expense(models.Model):
    vendor = models.ForeignKey(vendor,on_delete=models.CASCADE, null = True)
    employee = models.ForeignKey(employee,on_delete=models.CASCADE, null=True)
    expense_comment = models.CharField(max_length=100)
    expense_done_on = models.DateField(validators=[
        validators.MaxValueValidator(date.today, message='expense_done_on must not be after today\'s date'),
    ])
    expense_amount = models.IntegerField()
    
    def __str__(self):
        return self.expense_comment