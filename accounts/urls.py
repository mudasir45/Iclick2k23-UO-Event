from django.urls import path
from . import views


urlpatterns = [
    path('userSignUp/', views.userSignUp, name='userSignUp'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('alert', views.alert, name='alert'),
    path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
    path('resetRequest/', views.resetRequest, name='resetRequest'),
    path('confirmReset/<uuid:token>/', views.confirmReset, name='confirmReset'),
] 
