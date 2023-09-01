from django.urls import path 
from . import views

urlpatterns = [
    path('projectList/', views.projectList, name='projectList'),
]