from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import UserProfile
from .models import Problem, POTDStatus
import datetime
from django.urls import reverse
from pyscripts import codechef_scraping
# Create your views here.
#All the platforms will be here
def codechef(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("You need to be logged in to access this page.")
    
    user_profile = UserProfile.objects.get(user=user)
    problem = Problem.objects.filter(platform_id=1)  # Get the problems for CodeChef

    today = datetime.date.today()
    potd = problem.filter(assigned_date=today)[0] #this is the problem of the day
    past_problems = problem.filter(assigned_date__lt=today).order_by("-assigned_date") #this is the past problems
    iscodechef = True
    if user_profile.codechef_id is not None and user_profile.codechef_id != "":
        iscodechef = False
    # print(potd)
    context = {
        'user_profile': user_profile,
        'potd': potd,
        'past_problems': past_problems,
        'iscodechef': iscodechef,
    }
    return render(request, 'codechef.html', context)

def codeforces(request):
    return HttpResponse("Still making this page")

def refresh_potd_status(request):
    print("Refreshing POTD status for CodeChef")
    if request.method=="POST":
        user = request.user
        alreadydone = POTDStatus.objects.filter(user=user, platform_id=1, date=datetime.date.today()).first()
        if alreadydone:
            print(f"{user.username} have already solved the potd. Get lost. Dont waste my resources")
            return redirect(reverse('codechef'))
        else:
            user_profile = UserProfile.objects.get(user=user)
            potd = Problem.objects.filter(platform_id=1, assigned_date=datetime.date.today()).first()
            issolved = codechef_scraping.submissions(user_profile.codechef_id,potd.problem_id)
            print(issolved)
            POTDStatus.objects.create(
                user=user,
                platform_id=1,
                problem_id=potd.problem_id,
                date=datetime.date.today(),
                is_solved=issolved
            )

    return redirect(reverse('codechef'))