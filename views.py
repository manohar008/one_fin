from django.http import JsonResponse
from .models import employee,vendor,expense
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import F
from datetime import datetime
import re

@api_view(['GET'])
def getEmployees(request):
    employees = employee.objects.all()
    serializer = employeeSerializer(employees, many=True)
    return Response(serializer.data, stst)


@api_view(['GET'])
def getEmployee(request):
    employee_code = request.GET.get('employee_code')
    try:
        employees = employee.objects.filter(employee_code__icontains=employee_code)
        serializer = employeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except employee.DoesNotExist:
        return Response({"message": "employee not found"},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def addEmployee(request):
    serializer = employeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "employee created."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getVendors(request):
    vendors = vendor.objects.all()
    serializer = vendorSerializer(vendors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getVendor(request):
    vendor_code = request.GET.get('vendor_code')
    try:
        vendors = vendor.objects.filter(vendor_code__icontains=vendor_code)
        serializer = vendorSerializer(vendors,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({"message": "vendor not found"},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def addVendor(request):
    serializer = vendorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "vendor created."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getExpenses(request):
    expenses = expense.objects.all()
    serializer = expenseSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addExpense(request):
    expense_data = request.data
    new_expense = expense.objects.create(vendor=vendor.objects.get(vendor_code=expense_data['vendor_code']),
                                        employee=employee.objects.get(employee_code=expense_data['employee_code']),
                                        expense_comment=expense_data['expense_comment'],
                                        expense_done_on=expense_data['expense_done_on'],
                                        expense_amount=expense_data['expense_amount'])
    new_expense.expense_done_on = datetime.strptime(expense_done_on, '%d-%b-%y')
    new_expense.save()
    serializer = expenseSerializer(new_expense)
    return Response({"message": "expense created."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getExpenseForEmployee(request):
    employee_code = request.GET.get('employee_code', '').strip().upper()
    response = {}
    if employee_code:
        try:
            emp = employee.objects.get(employee_code = employee_code)
            response['name'] = emp.name
            # Using annotate to refer to vendor_code.name as vendor
            expenses = emp.expense_set.annotate(Vendor=F('vendor_id__name'))
            response['expenses'] = list(expenses.values('Vendor','expense_comment', 'expense_done_on', 'expense_amount'))
        except ObjectDoesNotExist as does_not_exist:
            response['message'] = str(does_not_exist)
    else:
        response['message'] = 'Please provide an employee_code.'
    return JsonResponse(response)

@api_view(['GET'])
def getExpenseForVendor(request):
    vendor_code = request.GET.get('vendor_code', '').strip().upper()
    response = {}
    if vendor_code:
        try:
            vend = vendor.objects.get(vendor_code = vendor_code)
            response['name'] = vend.name
            # Using annotate to refer to employee_code.name as employee
            expenses = vend.expense_set.annotate(Employee=F('employee_id__name'))
            response['expenses'] = list(expenses.values('Employee', 'expense_comment', 'expense_done_on', 'expense_amount'))
        except ObjectDoesNotExist as does_not_exist:
            response['message'] = str(does_not_exist)
    else:
        response['message'] = 'Please provide a vendor_code.'
    return JsonResponse(response)