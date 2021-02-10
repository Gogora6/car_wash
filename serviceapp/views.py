from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Sum

from .models import Order, Car, WashType
from user.choices import Status
from user.models import User

from .forms import OrderForm


def index(request: WSGIRequest) -> HttpResponse:
    return render(request, template_name='pages/index.html')


def washer_list(request: WSGIRequest) -> HttpResponse:
    washers = User.objects.filter(status=Status.washer).all()

    return render(request, template_name='pages/washers.html',
                  context={
                      'washers': washers
                  })


def washer_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    washer = get_object_or_404(User.objects.filter(status=Status.washer.value), pk=pk)

    filter_day = request.GET.get('filter')

    now = timezone.now()

    if filter_day:
        filter_date = now - timezone.timedelta(days=int(filter_day))
        orders = Order.objects.filter(employee=pk, end_date__isnull=False, start_date__gte=filter_date)
    else:
        orders = Order.objects.filter(employee=pk, end_date__isnull=False)

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


def order_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)

    return render(request, template_name='pages/order_details.html', context={
        'order': order
    })


def create_order(request: WSGIRequest) -> HttpResponse:
    order_form = OrderForm()
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order: Order = order_form.save(commit=False)
            order.booth_id = 1
            order.save()
            return redirect('wash:order_detail', order.pk)

    return render(request,
                  'pages/order-form.html',
                  context={'form': order_form})
