from django.shortcuts import render, redirect
from django.http import HttpResponse


def projectList(request):
    return render(request, 'projectList.html')

