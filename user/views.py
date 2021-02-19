from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import CustomUserRegistrationForm
from .models import User
from .choices import Status


def user_login(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('wash:index')
    login_form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            redirect_page_path = request.POST.get('redirectPage')
            if redirect_page_path:
                return redirect(redirect_page_path)

            return redirect('wash:index')

    return render(request, 'pages/users/login.html', context={'form': login_form})


def user_logout(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
    raise HttpResponse(status=405)


def user_register(request: WSGIRequest) -> HttpResponse:
    registration_form = CustomUserRegistrationForm()
    if request.method == 'POST':
        registration_form = CustomUserRegistrationForm(request.POST, files=request.FILES)
        if registration_form.is_valid():
            user: User = registration_form.save(commit=False)
            user.status = Status.customer
            user.save()
            return redirect('user:user_login')
    return render(request, 'pages/users/register.html', context={'form': registration_form})
