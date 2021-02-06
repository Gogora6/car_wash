from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q
from user.choices import Status
from user.models import User
from .models import Order
from django.utils import timezone


def index(request):
    return render(request, template_name='pages/index.html')


def washer_list(request):
    washers = User.objects.filter(status=Status.washer).all()

    return render(request, template_name='pages/washers.html',
                  context={
                      'washers': washers
                  })


def washer_detail(request, pk):
    washer = get_object_or_404(User.objects.filter(status=Status.washer.value), pk=pk)

    filter_day = request.GET.get('filter')

    now = timezone.now()

    if filter_day:
        filter_date = now - timezone.timedelta(days=int(filter_day))
        orders = Order.objects.filter(employee=pk, start_date__gte=filter_date)
    else:
        orders = Order.objects.filter(employee=pk)

    bonus = 0
    if orders.exists():
        sum_prices = orders.aggregate(Sum('price'))['price__sum']
        bonus = sum_prices * washer.share / 100

    return render(request, template_name='pages/washer_details.html', context={
        'orders': orders,
        'washer': washer,
        'bonus_money': bonus,
        'filter_day': filter_day
    })
