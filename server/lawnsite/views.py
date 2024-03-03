from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path

@csrf_exempt
def login(request):
    print("login")
    retirn JsonResponse({"Message":"Hello World"})

urlpatterns = [
    path("/login", login, name='login_post')
]
