from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
    return render(request, 'main/index.html')

def info(request):
    return render(request, 'alerts/info.html')

