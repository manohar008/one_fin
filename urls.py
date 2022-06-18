"""expensesapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expensesapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-employees/', views.getEmployees),
    path('get-employee/', views.getEmployee),
    path('add-employee/', views.addEmployee),
    path('get-vendors/', views.getVendors),
    path('get-vendor/', views.getVendor),
    path('add-vendor/', views.addVendor),
    path('get-expenses/', views.getExpenses),
    path('add-expense/', views.addExpense),
    path('get-expense-for-employee/', views.getExpenseForEmployee),
    path('get-expense-for-vendor/', views.getExpenseForVendor),
]
