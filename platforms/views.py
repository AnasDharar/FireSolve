from django.shortcuts import render, redirect
from django.http import HttpResponse
from psycopg2 import IntegrityError
from users.models import UserProfile
from django.contrib.auth.models import User 
from .models import Platform, Problem, POTDStatus
import datetime
from django.urls import reverse
from pyscripts import codechef_scraping
from pyscripts import codeforces_scraping
from .forms import BulkProblemForm
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def codechef(request):
    platform_id=1
    user = request.user
    platform = "CodeChef"
    if not user.is_authenticated:
        signup_url = reverse('signup')
        login_url = reverse('login')
        return HttpResponse(f"You have not logged in bro. go here -> <a href='{signup_url}'>Signup</a> or <a href='{login_url}'>Login</a>")

    user_profile = UserProfile.objects.get(user=user)

    if user_profile.codechef_id is None or user_profile.codechef_id == "":
        return render(request, 'usernamemissing.html', {'platform': platform})
    
    problem = Problem.objects.filter(platform_id=platform_id)  # Get the problems for CodeChef
    alreadydone = POTDStatus.objects.filter(user=user, solved_date=datetime.date.today()).first()
    today = datetime.date.today()
    try:
        potd = problem.filter(assigned_date=today)[0] #this is the problem of the day
    except IndexError:
        potd = None
    # if not potd:
    #     messages.error(request, "No Problem of the Day assigned for today.")    
    #     return redirect(reverse('codeforces'))
    past_problems = problem.filter(assigned_date__lt=today).order_by("-assigned_date") #this is the past problems
    leaderboard = UserProfile.objects.all().order_by('-total_solved')[:10]
    
    context = {
        'platform': platform,
        'id': platform_id,
        'user_profile': user_profile,
        'url':'https://www.codechef.com/problems/',
        'potd': potd,
        'past_problems': past_problems,
        'alreadydone': alreadydone,
        'leaderboard': leaderboard,
    }
    return render(request, 'solve.html', context)

def codeforces(request):
    platform_id=2
    user = request.user
    platform = "Codeforces"
    if not user.is_authenticated:
        signup_url = reverse('signup')
        login_url = reverse('login')
        return HttpResponse(f"You have not logged in bro. go here -> <a href='{signup_url}'>Signup</a> or <a href='{login_url}'>Login</a>")
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.codeforces_id is None or user_profile.codeforces_id == "":
        return render(request, 'usernamemissing.html', {'platform': platform})
    
    problem = Problem.objects.filter(platform_id=platform_id)  # Get the problems for Codeforces
    alreadydone = POTDStatus.objects.filter(user=user, solved_date=datetime.date.today()).first()
    today = datetime.date.today()
    try:
        potd = problem.filter(assigned_date=today)[0] #this is the problem of the day
    except IndexError:
        potd = None
    # if not potd:
    #     messages.error(request, "No Problem of the Day assigned for today.")    
    #     return redirect(reverse('codeforces'))
    past_problems = problem.filter(assigned_date__lt=today).order_by("-assigned_date") #this is the past problems
    leaderboard = UserProfile.objects.all().order_by('-total_solved')[:10]
    # print(potd)
    context = {
        'platform': platform,
        'id': platform_id,
        'user_profile': user_profile,
        'url':'https://codeforces.com/problemset/problem/',
        'potd': potd,
        'past_problems': past_problems,
        'alreadydone': alreadydone,
        'leaderboard': leaderboard,
    }
    return render(request, 'solve.html', context)


def refresh_potd_status(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to refresh the POTD status.")
        return redirect(reverse('codechef'))

    if request.method=="POST":
        platform_id = request.POST.get('platform_id')
        logger.info(f"Refreshing POTD status for platform ID: {platform_id} for user: {request.user.username}")
        user = request.user
        logger.info(f"Refreshing POTD status for platform ID: {platform_id} for user: {request.user.username}")

        # Rate limiting: Check if user made a request in the last 30 seconds
        from django.core.cache import cache
        cache_key = f"potd_refresh_{user.id}"
        if cache.get(cache_key):
            messages.warning(request, "Please wait before checking again.")
            if platform_id == '1':
                return redirect(reverse('codechef'))
            elif platform_id == '2':
                return redirect(reverse('codeforces'))
        
        # Set cache for 30 seconds
        cache.set(cache_key, True, 30)
        
        # Use atomic transaction to ensure data consistency
        with transaction.atomic():
            # Re-check within transaction to prevent race conditions
            alreadydone = POTDStatus.objects.filter(user=user, solved_date=datetime.date.today()).first()
            if alreadydone:
                # print(f"{user.username} have already solved the potd. Get lost. Dont waste resources")
                logger.info(f"{user.username} has already solved today's Problem of the Day.")
                messages.success(request, "Congratulations 🎉 You have already solved today's Problem of the Day.")
                if platform_id == '1':
                    return redirect(reverse('codechef'))
                elif platform_id == '2':
                    return redirect(reverse('codeforces'))
            
            user_profile = UserProfile.objects.select_for_update().get(user=user)
            potd = Problem.objects.filter(platform_id=platform_id, assigned_date=datetime.date.today()).first()
            if not potd:
                messages.error(request, "No Problem of the Day assigned for today.")
                if platform_id == '1':
                    return redirect(reverse('codechef'))
                elif platform_id == '2':
                    return redirect(reverse('codeforces'))
            if platform_id=="1":
                issolved = codechef_scraping.submissions(user_profile.codechef_id, potd.problem_id)
                
                if issolved:
                    # print(f"codechef scraping complete: {user.username} solved the potd")
                    logger.info(f"CodeChef scraping complete: {user.username} solved the Problem of the Day.")
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

                        logger.info(f"POTD status created for {user.username}, streak: {user_profile.codechef_streak}")
                        messages.success(request, f"You have successfully solved the Problem of the Day! Streak: {user_profile.codechef_streak}")
                            
                    except IntegrityError:
                        logger.warning(f"IntegrityError caught for user {user.username}: already solved today's Problem of the Day.")
                        messages.success(request, "Congratulations 🎉 You have already solved today's Problem of the Day.")
                    except Exception as e:
                        logger.error(f"Error creating POTD status for user {user.username}: {e}")
                        messages.error(request, "An error occurred while updating your status.")
                else:
                    logger.info(f"CodeChef scraping complete: {user.username} did not solve the Problem of the Day.")
                    messages.error(request, "You have not solved today's Problem of the Day")
            elif platform_id=="2":
                contestId,probIndex = potd.problem_id.split('/')
                issolved = codeforces_scraping.check_user(user_profile.codeforces_id,contestId,probIndex)
                
                if issolved:
                    logger.info(f"Codeforces scraping complete: {user.username} solved the Problem of the Day.")
                    try:
                        if POTDStatus.objects.filter(user=user, problem=potd).exists():
                            messages.success(request, "Congratulations 🎉 You have already solved today's Problem of the Day.")
                            return redirect(reverse('codeforces'))

                        POTDStatus.objects.create(
                            user=user,
                            problem=potd,
                            solved_date=datetime.date.today(),
                        )

                        user_profile.codeforces_streak += 1
                        user_profile.total_solved += 1
                        user_profile.save(update_fields=['codeforces_streak', 'total_solved'])

                        logger.info(f"POTD status created for {user.username}, streak: {user_profile.codeforces_streak}")
                        messages.success(request, f"You have successfully solved the Problem of the Day! Streak: {user_profile.codeforces_streak}")

                    except IntegrityError:
                        logger.warning(f"IntegrityError caught for user {user.username}: already solved today's Problem of the Day.")
                        messages.success(request, "Congratulations 🎉 You have already solved today's Problem of the Day.")
                    except Exception as e:
                        logger.error(f"Error creating POTD status for user {user.username}: {e}")
                        messages.error(request, "An error occurred while updating your status.")
                else:
                    logger.info(f"Codeforces scraping complete: {user.username} did not solve the Problem of the Day.")
                    messages.error(request, "You have not solved today's Problem of the Day")
    if platform_id == '1':
        return redirect(reverse('codechef'))
    elif platform_id == '2':
        return redirect(reverse('codeforces'))

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
                    logger.error(f"Error adding problem {problem_id}: {e}")
            messages.success(request, f"{added} problems added successfully.")
            return redirect('addproblems')
    # if a GET request is made, we will create a blank form
    else:
        form = BulkProblemForm()
    return render(request, 'bulk-add.html', {'form': form})