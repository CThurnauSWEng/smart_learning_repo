from django.shortcuts import render, HttpResponse, redirect
from ..user_app.models import User
from ..editor_app.models import Subject, Card
from django.core import serializers

import math

def learner_home(request):
    context = {
        'this_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "learner_app/learner_home.html",context)
   

def learner_dashboard(request):
    # gather data about subjects this user is studying
    this_user = User.objects.get(id=request.session['user_id'])
    this_users_subjects = this_user.subjects_studying.all()
    num_subjects = len(this_users_subjects)

    # gather list of subjects this user is not yet studying
    this_users_subjects_id = this_user.subjects_studying.all().values('id')
    other_subjects = Subject.objects.exclude(id__in=this_users_subjects_id)

    context = {
        'this_user'      : this_user,
        'other_subjects' : other_subjects,
        'num_subjects'   : num_subjects
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

    if len(cards) < 1:
        return redirect('/learner/learner_dashboard')

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
    request.session['total_correct']    = 0
    card_stats[0]['card_visited']       = True

    cur_card = Card.objects.get(id=card_stats[0]['card_id'])
    context = {
        'status'   : 'none',
        'cur_card' : cur_card
    }

    return render (request, 'learner_app/quiz_card.html', context)

def check_answer(request):
    cur_card = Card.objects.get(id=request.session['card_id'])

    card_answer = ""
    for idx in range(0,len(cur_card.answer)):
        if (cur_card.answer[idx] != " "):
            card_answer = card_answer + cur_card.answer[idx]
    clean_card_answer = card_answer.lower()

    user_answer = ""
    for idx in range(0,len(request.POST['learner_answer'])):
        if (request.POST['learner_answer'][idx] != " "):
            user_answer = user_answer + request.POST['learner_answer'][idx]
    clean_user_answer = user_answer.lower()

    if clean_user_answer == clean_card_answer:
        request.session['total_correct'] += 1
        request.session['card_stats'][request.session['card_stats_idx']]['answer_correct'] = True
        context = {
            'status'    : 'Correct!',
            'cur_card'  : cur_card
        }
    else:
        context = {
            'status'    : 'Please Try Again',
            'cur_card'  : cur_card
        }   
    return render (request, 'learner_app/quiz_card.html', context)

def display_next_card(request):
    if request.session['card_stats_idx'] != (len(request.session['card_stats'])-1):
        request.session['card_stats_idx'] += 1
        request.session['card_id'] = request.session['card_stats'][request.session['card_stats_idx']]['card_id']
        request.session['card_stats'][request.session['card_stats_idx']]['card_visited'] = True
    else:
        # no more cards
        total_cards = float(len(request.session['card_stats']))
        total_correct = float(request.session['total_correct'])
        percent_correct = int(((total_correct/total_cards)*10000)/100)
        # user can repeat a card if desired for practice, but the repeats should not
        # result in a score greater than 100%
        if percent_correct > 100:
            percent_correct = 100

        this_user = User.objects.get(id=request.session['user_id'])

        if percent_correct > 90:
            message = "Great Job " + this_user.first_name + "!"
        elif percent_correct > 80:
            message = "Good Job " + this_user.first_name + "!"
        elif percent_correct > 70:
            message = "Pretty good job, " + this_user.first_name
        else:
            message = "Thanks for playing " + this_user.first_name


        context = {
            'this_user'         : this_user,
            'percent_correct'   : percent_correct,
            'message'           : message
        }
        return render (request, 'learner_app/quiz_complete.html',context)
    
    cur_card = Card.objects.get(id=request.session['card_id'])
    context = {
        'status'   : 'none',
        'cur_card' : cur_card
    }
    return render (request, 'learner_app/quiz_card.html', context)
    
def show_answer(request):
    card = Card.objects.filter(id=request.session['card_id'])
    card_json = serializers.serialize("json",card)
    return HttpResponse(card_json, content_type='application/json')
