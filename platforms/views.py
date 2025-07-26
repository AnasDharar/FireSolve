from django.shortcuts import render, redirect
from django.http import HttpResponse
from psycopg2 import IntegrityError
from users.models import UserProfile
from django.contrib.auth.models import User 
from .models import Platform, Problem, POTDStatus
import datetime
from django.urls import reverse
from pyscripts import codechef_scraping
from .forms import BulkProblemForm
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
# Create your views here.
#All the platforms will be here
def codechef(request):
    user = request.user

    if not user.is_authenticated:
        signup_url = reverse('signup')
        login_url = reverse('login')
        return HttpResponse(f"You have not logged in bro. go here -> <a href='{signup_url}'>Signup</a> or <a href='{login_url}'>Login</a>")

    user_profile = UserProfile.objects.get(user=user)
    problem = Problem.objects.filter(platform_id=1)  # Get the problems for CodeChef
    alreadydone = POTDStatus.objects.filter(user=user, solved_date=datetime.date.today()).first()
    today = datetime.date.today()
    potd = problem.filter(assigned_date=today)[0] #this is the problem of the day
    past_problems = problem.filter(assigned_date__lt=today).order_by("-assigned_date") #this is the past problems
    leaderboard = UserProfile.objects.all().order_by('-total_solved')[:10]
    iscodechef = True
    if user_profile.codechef_id is not None and user_profile.codechef_id != "":
        iscodechef = False
    # print(potd)
    context = {
        'user_profile': user_profile,
        'potd': potd,
        'past_problems': past_problems,
        'iscodechef': iscodechef,
        'alreadydone': alreadydone,
        'leaderboard': leaderboard,
    }
    return render(request, 'codechef.html', context)

def codeforces(request):
    return HttpResponse("Coming soon. Codeforces is not implemented yet.")

def refresh_potd_status(request):
    print("Refreshing POTD status for CodeChef for user:", request.user.username)
    if request.method=="POST":
        user = request.user
        
        # Rate limiting: Check if user made a request in the last 30 seconds
        from django.core.cache import cache
        cache_key = f"potd_refresh_{user.id}"
        if cache.get(cache_key):
            messages.warning(request, "Please wait before checking again.")
            return redirect(reverse('codechef'))
        
        # Set cache for 30 seconds
        cache.set(cache_key, True, 30)
        
        # Use atomic transaction to ensure data consistency
        with transaction.atomic():
            # Re-check within transaction to prevent race conditions
            alreadydone = POTDStatus.objects.filter(user=user, solved_date=datetime.date.today()).first()
            if alreadydone:
                print(f"{user.username} have already solved the potd. Get lost. Dont waste resources")
                messages.success(request, "Congratulations 🎉 You have already solved today's Problem of the Day.")
                return redirect(reverse('codechef'))
            
            user_profile = UserProfile.objects.select_for_update().get(user=user)
            potd = Problem.objects.filter(platform_id=1, assigned_date=datetime.date.today()).first()
            
            if not potd:
                messages.error(request, "No Problem of the Day assigned for today.")
                return redirect(reverse('codechef'))
            
            issolved = codechef_scraping.submissions(user_profile.codechef_id, potd.problem_id)
            
            if issolved:
                print(f"codechef scraping complete: {user.username} solved the potd")
                try:
                    # Double-check again within the transaction
                    if POTDStatus.objects.filter(user=user, problem=potd).exists():
                        messages.success(request, "Congratulations 🎉 You have already solved today's Problem of the Day.")
                        return redirect(reverse('codechef'))
                    
                    # Create the status record
                    POTDStatus.objects.create(
                        user=user,
                        problem=potd,
                        solved_date=datetime.date.today(),
                    )
                    
                    # Increment streak
                    user_profile.codechef_streak += 1
                    user_profile.total_solved += 1
                    user_profile.save(update_fields=['codechef_streak', 'total_solved'])

                    print(f"POTD status created for {user.username}, streak: {user_profile.codechef_streak}")
                    messages.success(request, f"You have successfully solved the Problem of the Day! Streak: {user_profile.codechef_streak}")
                        
                except IntegrityError:
                    print("YOU HAVE ALREADY SOLVED THE PROBLEM TODAY - IntegrityError caught")
                    messages.success(request, "Congratulations 🎉 You have already solved today's Problem of the Day.")
                except Exception as e:
                    print(f"Error creating POTD status: {e}")
                    messages.error(request, "An error occurred while updating your status.")
            else:
                print(f"codechef scraping complete: {user.username} did not solve the potd")
                messages.error(request, "You have not solved today's Problem of the Day")
            

    return redirect(reverse('codechef'))

def addproblems(request):
    if not request.user.is_staff:
        return HttpResponse("You are not authorized view this page.")
    if request.method == "POST":
        form = BulkProblemForm(request.POST)
        if form.is_valid():
            raw = form.cleaned_data['raw_data']
            lines = raw.strip().split('\n')
            added = 0
            for line in lines:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) != 5:
                    continue  # skip malformed rows
                platform, problem_id, title, solution_url, assigned_date = parts
                try:
                    assigned_date_obj = datetime.datetime.strptime(assigned_date, "%Y-%m-%d").date()
                    Problem.objects.create(
                        platform=Platform.objects.get(id=int(platform)),
                        problem_id=problem_id,
                        title=title,
                        solutionurl=solution_url,
                        assigned_date=assigned_date_obj
                    )
                    added += 1
                except Exception as e:
                    print(f"Error adding problem {problem_id}: {e}")
            messages.success(request, f"{added} problems added successfully.")
            return redirect('addproblems')
    # if a GET request is made, we will create a blank form
    else:
        form = BulkProblemForm()
    return render(request, 'bulk-add.html', {'form': form})