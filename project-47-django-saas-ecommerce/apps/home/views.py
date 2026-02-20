from django.shortcuts import render
from django.http import HttpResponse
import requests

# display users 
def home(request):
    return render(request, "home/index.html")

