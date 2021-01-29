from django.shortcuts import render, HttpResponse
from .models import Employee, Orders
import datetime


def index(request):
    return render(request, template_name='pages/index.html')


def team(request):
    employees = Employee.objects.all()
    return render(request, template_name='pages/team.html',
                  context={
                      'employees': employees
                  })


def employee(request, pk, filter_day=365):
    filter_date = datetime.datetime.now() - datetime.timedelta(days=filter_day)
    orders = Orders.objects.filter(employee=pk, time__gte=filter_date)
    employee_detail = Employee.objects.filter(pk=pk).first()
    return render(request, template_name='pages/employee.html', context={
        'orders': orders,
        'employee': employee_detail
    })
