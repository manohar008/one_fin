from rest_framework import serializers
from .models import employee,vendor,expense

class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = ['name','employee_code']

class vendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendor
        fields = ['name','vendor_code']

class expenseSerializer(serializers.ModelSerializer):
    vendor = vendorSerializer(many=False,read_only=True)
    employee = employeeSerializer(many=False,read_only=True)
    class Meta:
        model = expense
        fields = ['vendor','employee','expense_comment','expense_done_on','expense_amount']

