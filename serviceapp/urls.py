from django.urls import path
from .views import index, washer_list, washer_detail


app_name = 'wash'
urlpatterns = [
    path('', index, name='index'),
    path('washers', washer_list, name='washers'),
    path('<int:pk>/washer', washer_detail, name='washer_detail'),
]

