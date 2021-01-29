from django.shortcuts import render, HttpResponse
from .models import Employee


def index(request):
    data = [[1, 2, 3], [5, 4, 2], (1, 5, 6)]
    return render(request, template_name='pages/index.html', context={
        'data': data
    })


def team(request):
    employees = Employee.objects.all()
    return render(request, template_name='pages/team.html',
                  context={
                      'employees': employees
                  })


def employee(request, pk):
    return HttpResponse(pk)
