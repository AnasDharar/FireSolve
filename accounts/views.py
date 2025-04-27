from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from users.models import UserProfile
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def signup(request):
    if request.method == "POST":
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # try:
        user = User.objects.create_user(first_name = f_name, last_name = l_name,email=email,username=username, password=password)
        user_profile = UserProfile.objects.create(user=user, first_name=f_name, last_name=l_name, email=email)
        user_profile.save()
        user.save()
        messages.info(request,'User created successfully')
        return redirect(reverse('login'))
        # except IntegrityError:
        #     print("Username already exists")
        #     print(IntegrityError)
        #     messages.error(request,'Username already exists')

    return render(request, 'signup.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard'))
        else:
            print("Invalid credentials")
    
    return render(request, 'login.html')
        
def logoutUser(request):
    logout(request)
    return redirect(reverse('landing'))

