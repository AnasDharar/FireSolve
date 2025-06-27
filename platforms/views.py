from django.shortcuts import render
from django.http import HttpResponse
from users.models import UserProfile
from .models import Problem, POTDStatus
import datetime
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
    print(potd)
    context = {
        'user_profile': user_profile,
        'potd': potd,
        'past_problems': past_problems,
        'iscodechef': iscodechef,
    }
    return render(request, 'codechef.html', context)

def codeforces(request):
    return HttpResponse("Still making this page")
