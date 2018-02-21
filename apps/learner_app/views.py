from django.shortcuts import render, HttpResponse, redirect
from ..user_app.models import User

def learner_home(request):
    context = {
        'this_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "learner_app/learner_home.html",context)
   

def learner_dashboard(request):
    context = {
        'this_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "learner_app/learner_dashboard.html",context)

