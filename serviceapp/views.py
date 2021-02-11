from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum

from .models import Order, Car, WashType
from user.choices import Status
from user.models import User

from .forms import OrderForm, CarForm


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


def orders_list(request: WSGIRequest) -> HttpResponse:
    finish_filter = request.GET.get('finished', None)
    page = request.GET.get('page', 1)

    orders: Order = Order.objects.filter().order_by('-start_date').all()

    if finish_filter:
        orders: Order = Order.objects.filter(end_date__isnull=finish_filter).order_by('-start_date').all()

    paginator = Paginator(orders, 12)
    orders = paginator.page(page)

    return render(request, 'pages/orders.html', context={'orders': orders})


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


def cars_list(request: WSGIRequest) -> HttpResponse:
    car_list = Car.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(car_list, 12)
    cars = paginator.page(page)

    car_form = CarForm()
    message_text = None
    if request.method == 'POST':
        car_form = CarForm(request.POST)
        if car_form.is_valid():
            car: Car = car_form.save(commit=False)
            car.save()
            message_text = f'Car Successfully added!'
            car_form = CarForm()
    return render(request, 'pages/cars.html', context={'cars': cars, 'form': car_form, 'message': message_text})
