from django.shortcuts import render
from django.http import HttpResponse
import requests

# display users 
def users(request):
    #pull data from third party rest api
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    #convert reponse data into json
    users = response.json()
    print(users)
    
    # return HttpResponse(users)
    return render(request, "payments/users.html", {'users': users})

