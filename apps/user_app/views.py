from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages

# the index function is called when root is visited
def index(request):
    return render(request, "user_app/index.html")

def process_login(request):

    response = User.objects.validate_login_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        request.session['name']    = response['user'].first_name
        request.session['user_id'] = response['user'].id
        return redirect('/learner/learner_home')
    else:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')


def process_register(request):
    
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.

    response = User.objects.validate_registration_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        request.session['name']    = response['user'].first_name
        request.session['user_id'] = response['user'].id
        return redirect('/learner/learner_home')
    else:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')

def logout(request):
    request.session['errors']  = []
    request.session['name']    = ''
    request.session['user_id'] = 0
    return redirect('/')
