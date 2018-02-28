from django.shortcuts import render, HttpResponse, redirect
from ..user_app.models import User
from ..editor_app.models import Subject, Card
from django.core import serializers

def learner_home(request):
    context = {
        'this_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "learner_app/learner_home.html",context)
   

def learner_dashboard(request):
    this_user = User.objects.get(id=request.session['user_id'])
    this_users_subjects_id = this_user.subjects_studying.all().values('id')
    other_subjects = Subject.objects.exclude(id__in=this_users_subjects_id)

    context = {
        'this_user'      : this_user,
        'other_subjects' : other_subjects
    }
    return render(request, "learner_app/learner_dashboard.html",context)

def add_subject(request, subject_id):
    this_subject = Subject.objects.get(id=subject_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.subjects_studying.add(this_subject)
    return redirect ('/learner/learner_dashboard')

def remove(request, subject_id):
    this_subject = Subject.objects.get(id=subject_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.subjects_studying.remove(this_subject)
    return redirect ('/learner/learner_dashboard')

def start_quiz(request, subject_id):
    this_subject = Subject.objects.get(id=subject_id)

    card_stats = []
    cards = Card.objects.filter(subject=this_subject)
    for card in cards:
        card_object = {
            'card_id'       : card.id,
            'card_visited'  : False,
            'answer_correct': False,
        }
        card_stats.append(card_object)


    request.session['cur_subject_id']   = subject_id
    request.session['card_stats']       = card_stats
    request.session['card_stats_idx']   = 0
    request.session['card_id']          = card_stats[0]['card_id']
    card_stats[0]['card_visited']       = True

    cur_card = Card.objects.get(id=card_stats[0]['card_id'])
    context = {
        'status'   : 'none',
        'cur_card' : cur_card
    }

    return render (request, 'editor_app/quiz_card.html', context)

def check_answer(request):
    cur_card = Card.objects.get(id=request.session['card_id'])
    if request.POST['card_answer'] == request.POST['learner_answer']:
        context = {
            'status'    : 'Correct!',
            'cur_card'  : cur_card
        }
    else:
        context = {
            'status'    : 'Please Try Again',
            'cur_card'  : cur_card
        }   
    return render (request, 'editor_app/quiz_card.html', context)

def display_next_card(request):
    if request.session['card_stats_idx'] != (len(request.session['card_stats'])-1):
        request.session['card_stats_idx'] += 1
        request.session['card_id'] = request.session['card_stats'][request.session['card_stats_idx']]['card_id']
        request.session['card_stats'][request.session['card_stats_idx']]['card_visited'] = True
        request.session['card_stats'][request.session['card_stats_idx']]['answer_correct'] = True
    else:
        # no more cards
        # temporarily return to dashboard. 
        # future - redirect or render page to display score
        return redirect('/learner/learner_dashboard')
    
    cur_card = Card.objects.get(id=request.session['card_id'])
    context = {
        'status'   : 'none',
        'cur_card' : cur_card
    }
    return render (request, 'editor_app/quiz_card.html', context)
    
def show_answer(request):
    print "in show answer"
    card = Card.objects.filter(id=request.session['card_id'])
    card_json = serializers.serialize("json",card)
    print "card_json: ", card_json
    return HttpResponse(card_json, content_type='application/json')
