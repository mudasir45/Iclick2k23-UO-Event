from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .emails import resert_send_mail_request

import uuid
from .models import profile

def userSignUp(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        current_user = User.objects.create_user(
            username=username,
            email=email,
            first_name = first_name,
            )
        current_user.set_password(password1)
        current_user.save()

        profile_obj = profile.objects.create(user = current_user)
        profile_obj.save()

        messages.success(request, 'Registration successfull! Login here')
        return redirect('userLogin')
    return render(request, 'accounts/userSignUp.html')

def check_username_availability(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'})
        else:
            return JsonResponse({'message': 'Username is available'})

def userLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        current_user = authenticate(request, username=username, password=password)
        if current_user is not None:
                login(request, current_user)
                next_url = request.GET.get('?next')
                print(next_url)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('home')
        else:
            return JsonResponse({'message':'Invalid Credientials'})
    return render(request, 'accounts/userLogin.html')
                 
def userLogout(request):
    logout(request)
    return redirect('home')


def alert(request):
    return render(request, 'alerts/alert.html')


def resetRequest(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        currentUser = None
        try:
            currentUser = User.objects.get(email = email)
        except:
            messages.error(request, 'Email does not exists')
            return HttpResponseRedirect(request.path_info)
        if currentUser:
            token = str(uuid.uuid4())
            try:
                resert_send_mail_request(email, token)
                user_profile = profile.objects.filter(user=currentUser).first()
                user_profile.token = token
                user_profile.save()
                messages.success(request, 'An Email has been sent to your email')
                return HttpResponseRedirect(request.path_info)
            except Exception as e:
                print(e)

        # return HttpResponse("reset request successful")
    return render(request, 'accounts/resetRequest.html')

def confirmReset(request, token):
    user_profile = profile.objects.get(token=token)
    if request.method == 'POST':
        newPass = request.POST.get('newPass')
        confPass = request.POST.get('confPass')
        if newPass != confPass:
            messages.error(request, 'New password and confirm password are not matched!')
            return HttpResponseRedirect(request.path_info)
        else:
            currentUser = user_profile.user
            currentUser.set_password(newPass)
            currentUser.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('home')
    context = {'token': token}
    return render(request, 'accounts/ResetPass.html', context)
