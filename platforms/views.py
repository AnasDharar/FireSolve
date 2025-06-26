from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#All the platforms will be here
def codechef(request):
    
    context = {

    }
    return render(request, 'codechef.html')

def codeforces(request):
    return HttpResponse("Still making this page")
