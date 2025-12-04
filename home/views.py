from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from users.models import UserProfile
from django.contrib.auth import authenticate,logout, login
from django.db import IntegrityError
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def dashboard(request):
    if request.user.is_anonymous==False:
        logger.info(f"User {request.user.username} logged in")
        user_profile = UserProfile.objects.get(user=request.user)
        leaderboard = UserProfile.objects.all().order_by('-ultimate_streak')[:10]
        # print(leaderboard)
        return render(request,'index2.html', {'user_data': user_profile, 'leaderboard': leaderboard})

    return redirect('/')
    
def landing(request):
    context = {'range1to9': range(1, 9),
               'range0to3': range(0, 3),
                }                 
    if request.user.is_anonymous:
        logger.info('Anonymous user accessing landing page')
        return render(request,'landing.html',context)
    
    return redirect('dashboard/')
        
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')