from django.urls import path
from .views import index, team, employee

urlpatterns = [
    path('', index, name='index'),
    path('our-team', team, name='our-team'),
    path('<int:pk>/employee/date_filter=<int:filter_day>', employee, name='employee_detail'),
]
