from django.urls import path

from .views import user_login, user_register, user_logout, user_dashboard

app_name = 'user'
urlpatterns = [
    path('login', user_login, name='user_login'),
    path('register', user_register, name='user_register'),
    path('logout', user_logout, name='user_logout'),
    path('profile', user_dashboard, name='user_dashboard')

]
