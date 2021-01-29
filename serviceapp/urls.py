from django.urls import path
from .views import index, team, employee

urlpatterns = [
    path('', index, name='index'),
    path('our-team', team, name='our-team'),
    path('<int:pk>/employee', employee, name='employee_detail'),
]
