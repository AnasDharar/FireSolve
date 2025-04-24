from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User 
# from .models import UserProfile
# Create your views here.
def profile_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'user_not_found.html', status=404)
    is_owner =  user==request.user
    
    user_data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_owner': is_owner,
        # Add more fields as needed
    }
    print(is_owner)
    print(user)
    print(request.user)
    return render(request, '../templates/profile.html', {'user': user_data})

def edit_profile_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'user_not_found.html', status=404)
    is_owner =  user==request.user
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        user_data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_owner': is_owner,
        # Add more fields as needed
        }
        return render(request, 'profile.html', {'user': user_data})
    return render(request, 'edit_profile.html', {'user': user})