from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import Employee

def index(request):
    employees = Employee.objects.all()
    return render(request, "client_app/client_index.html", {"employees": employees})


def create_employee(request):
    if request.POST:
        name = request.POST.get("name")
        employee = Employee(name=name)
        employee.save()
        return redirect("client_index")