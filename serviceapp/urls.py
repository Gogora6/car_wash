from django.urls import path
from .views import index, washer_list, washer_detail, create_order

app_name = 'wash'
urlpatterns = [
    path('', index, name='index'),
    path('washers/', washer_list, name='washers'),
    path('<int:pk>/washer/', washer_detail, name='washer_detail'),
    path('order/create', create_order, name='create_order')
]
