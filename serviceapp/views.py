from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from user.choices import Status
from user.models import User
from .models import Order
import datetime


def index(request):
    return render(request, template_name='pages/index.html')


def team(request):
    employees = User.objects.filter(status=Status.washer).all()

    return render(request, template_name='pages/team.html',
                  context={
                      'employees': employees
                  })


def employee(request, pk):
    employee_detail = get_object_or_404(User, pk=pk)

    filter_day = request.GET.get('filter')
    if filter_day:
        filter_date = datetime.datetime.now() - datetime.timedelta(days=int(filter_day))
        orders = Order.objects.filter(employee=pk, start_date__gte=filter_date).all()
    else:
        orders = Order.objects.filter(employee=pk).all()

    if len(orders) > 0:
        sum_prices = orders.aggregate(Sum('price'))['price__sum']

        bonus = sum_prices * employee_detail.share / 100
    else:
        bonus = 0
    return render(request, template_name='pages/employee.html', context={
        'orders': orders,
        'employee': employee_detail,
        'bonus_money': bonus,
        'filter_day': filter_day
    })
