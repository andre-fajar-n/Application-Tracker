from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='application_tracker:login')
def Home(request):
    context = {
        "is_dashboard":"active",
    }
    return render(request, 'home.html',context)
