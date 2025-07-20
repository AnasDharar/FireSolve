from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User 
from .models import UserProfile
# Create your views here.
def profile_view(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        return render(request, 'user_not_found.html', status=404)
    is_owner =  user==request.user
    
    user_data = {
        'username': user.username,
        'user_profile': user_profile,
        'email': user_profile.email,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'is_owner': is_owner,
        'codechef_id': user_profile.codechef_id,
        'codeforces_id': user_profile.codeforces_id,
        'leetcode_id': user_profile.leetcode_id,
        # Add more fields as needed
    }
    print('User',request.user.username,'viewed profile of',user.username)
    return render(request, 'profile.html', {'user_data': user_data})

def edit_profile_view(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        return render(request, 'user_not_found.html', status=404)
    is_owner =  user==request.user
    if is_owner == False:
        return HttpResponse("You are not authorized to edit this profile.", status=403)
    user_data = {
        'username': user.username,
        'email': user_profile.email,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'codechef_id': user_profile.codechef_id,
        'codeforces_id': user_profile.codeforces_id,
        'leetcode_id': user_profile.leetcode_id,
        'is_owner': is_owner,
        }
    if request.method == 'POST':
        user_profile.first_name = request.POST.get('first_name', user_profile.first_name)
        user_profile.last_name = request.POST.get('last_name', user_profile.last_name)
        user_profile.email = request.POST.get('email', user_profile.email)
        user_profile.codechef_id = request.POST.get('codechef_id', user_profile.codechef_id)
        user_profile.codeforces_id = request.POST.get('codeforces_id', user_profile.codeforces_id)
        user_profile.leetcode_id = request.POST.get('leetcode_id', user_profile.leetcode_id)
        user_profile.save()
        print('User',request.user.username,'edited profile')
        user_data = {
        'username': user.username,
        'email': user_profile.email,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'codechef_id': user_profile.codechef_id,
        'codeforces_id': user_profile.codeforces_id,
        'is_owner': is_owner,
        # Add more fields as needed
        }
        return redirect('profile', username=user.username)
    return render(request, 'edit_profile.html', {'user': user_data})