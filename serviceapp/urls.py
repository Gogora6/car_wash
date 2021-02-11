from django.urls import path
from .views import index, washer_list, washer_detail, create_order, order_detail, orders_list, cars_list

app_name = 'wash'
urlpatterns = [
    path('', index, name='index'),
    path('washers/', washer_list, name='washers'),
    path('<int:pk>/washer/', washer_detail, name='washer_detail'),
    path('orders', orders_list, name='orders'),
    path('order/create', create_order, name='create_order'),
    path('<int:pk>/order/', order_detail, name='order_detail'),
    path('cars', cars_list, name='cars'),

]
