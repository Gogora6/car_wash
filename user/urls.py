from django.urls import path

from .views import user_login, user_register, user_logout, user_dashboard

app_name = 'user'
urlpatterns = [
    path('login', user_login, name='login'),
    path('register', user_register, name='register'),
    path('logout', user_logout, name='logout'),
    path('profile', user_dashboard, name='dashboard')

]
