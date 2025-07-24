from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User 
from potd import settings
from users.models import UserProfile
from django.contrib.auth import authenticate, logout, login
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse
from accounts.forms import CustomUserCreationForm
from django.core.cache import cache
import time
# Create your views here.

def signup(request):
    # Rate limiting by IP
    ip_address = request.META.get('REMOTE_ADDR')
    cache_key = f"signup_attempts_{ip_address}"
    attempts = cache.get(cache_key, 0)
    
    if attempts >= 3:  # Max 3 signup attempts per hour per IP
        messages.error(request, "Too many signup attempts. Please try again later.")
        return render(request, 'signup.html', {'form': None})
    
    if request.method == "POST":
        # Increment attempt counter
        cache.set(cache_key, attempts + 1, 3600)  # 1 hour timeout
        
        form = CustomUserCreationForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        try:
            if form.is_valid():
                user = form.save()
                user_profile = UserProfile.objects.create(user=user, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'])
                messages.info(request,'User created successfully')
                # Clear attempt counter on successful signup
                cache.delete(cache_key)
                return redirect(reverse('login'))
            else:
                # Form is not valid, return with errors
                return render(request, 'signup.html', {'form': form, 'SIGNUP_SECRET_KEY': settings.SIGNUP_SECRET_KEY})
        except IntegrityError:
            print("Username already exists")
            messages.error(request,'Username already exists')
    else:
        # Initialize form with timestamp for timing validation
        initial_data = {
            'signup_secret_key': settings.SIGNUP_SECRET_KEY,
            'form_timestamp': str(time.time())
        }
        form = CustomUserCreationForm(initial=initial_data)
    return render(request, 'signup.html', {'form': form, 'SIGNUP_SECRET_KEY': settings.SIGNUP_SECRET_KEY})

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
            messages.error(request, 'Invalid credentials')
            return redirect(reverse('login'))
    
    return render(request, 'login.html')
        
def logoutUser(request):
    logout(request)
    return redirect(reverse('landing'))

