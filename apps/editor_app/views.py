from django.shortcuts import render, HttpResponse, redirect
from ..user_app.models import User
from .models import Subject, Card

# the index function is called when root is visited
def create_subject(request):
    context = {
        'this_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "editor_app/create_subject.html", context)

def process_create_subject(request):

    response = Subject.objects.validate_subject_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        request.session['subject_id'] = response['subject'].id
        return redirect('/editor/edit_subject/{}'.format(response['subject'].id))
    else:
        request.session['errors'] = response['errors']
        return render(request, "editor_app/create_subject.html")

def editor_dashboard(request):
    this_user = User.objects.get(id=request.session['user_id'])
    this_users_subjects = this_user.subjects_editing.all()
    num_subjects = len(this_users_subjects)

    context = {
        'this_user'     : this_user,
        'num_subjects'  : num_subjects
    }
    return render(request, "editor_app/editor_dashboard.html",context)

def edit_subject(request, subject_id):
    this_subject = Subject.objects.get(id=subject_id)
    request.session['subject_id'] = subject_id
    cards = Card.objects.filter(subject=this_subject)

    context = {
        'subject'   : this_subject,
        'cards'     : cards,
        'num_cards' : len(cards)
    }
    return render(request, "editor_app/edit_subject.html", context)

def create_card(request):
    context = {
        'this_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "editor_app/create_card.html", context)

def process_create_card(request):

    response = Card.objects.validate_card_data(request)

    if (response['status']):
        request.session['errors']  = []
        request.session['card_id'] = response['card'].id
        return redirect('/editor/edit_card/{}'.format(response['card'].id))
    else:
        request.session['errors'] = response['errors']
        return render(request, "editor_app/create_card.html")

def edit_card(request, card_id):
    this_card = Card.objects.get(id=card_id)
    context = {
        'this_card' : this_card
    }
    return render(request, "editor_app/edit_card.html", context)
