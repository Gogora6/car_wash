from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings

from .forms import CustomUserRegistrationForm
from .models import User
from .choices import Status


def user_login(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('user:dashboard')
    login_form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            redirect_page_path = request.POST.get('redirectPage')
            if redirect_page_path:
                return redirect(redirect_page_path)

            return redirect('user:dashboard')

    return render(request, 'pages/users/login.html', context={'form': login_form})


def user_logout(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
    raise HttpResponse(status=405)


def user_register(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('user:dashboard')
    registration_form = CustomUserRegistrationForm()
    if request.method == 'POST':
        registration_form = CustomUserRegistrationForm(request.POST, files=request.FILES)
        if registration_form.is_valid():
            user: User = registration_form.save(commit=False)
            user.status = Status.customer
            user.save()
            messages.success(request, 'Registration completed successfully!')

            return redirect('user:user_login')
    return render(request, 'pages/users/register.html', context={'form': registration_form})


@login_required(redirect_field_name='redirectPage')
def user_dashboard(request: WSGIRequest) -> HttpResponse:
    password_change_form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            messages.success(request, 'Password successfully changed.')

    return render(request, 'pages/users/dashboard.html', context={'form': password_change_form})
