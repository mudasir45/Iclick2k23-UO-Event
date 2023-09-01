from django.urls import path 
from . import views

urlpatterns = [

    # PROJECT CRUD URLS 
    path('projectList/', views.projectList, name='projectList'),
    path('addProject/', views.addProject, name='addProject'),
    path('updateProject/<str:slug>', views.updateProject, name='updateProject'),
    path('deleteProject/<str:slug>', views.deleteProject, name='deleteProject'),
    path('projectDetails/<str:slug>', views.projectDetails, name='projectDetails'),
   
    # GROUP CRUD URLS 
    path('addGroup/', views.addGroup, name='addGroup'),
    path('updateGroup/<str:uid>', views.updateGroup, name='updateGroup'),
    path('deleteGroup/<str:uid>', views.deleteGroup, name='deleteGroup'),
]