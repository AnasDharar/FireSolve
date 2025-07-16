from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import UserProfile
from .models import Platform, Problem, POTDStatus
import datetime
from django.urls import reverse
from pyscripts import codechef_scraping
from .forms import BulkProblemForm
from django.contrib import messages
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

def addproblems(request):
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