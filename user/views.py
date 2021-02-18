from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from .choices import Status
from .forms import CustomUserRegistrationForm
from .models import User


def user_register(request: WSGIRequest) -> HttpResponse:
    registration_form = CustomUserRegistrationForm()
    if request.method == 'POST':
        registration_form = CustomUserRegistrationForm(request.POST, files=request.FILES)
        if registration_form.is_valid():
            print('Valid')
            user: User = registration_form.save(commit=False)
            user.status = Status.customer
            user.save()
    return render(request, 'pages/users/register.html', context={'form': registration_form})
