from __future__ import unicode_literals
from django.db import models
from ..user_app.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import re

NAME_REGEX = re.compile(r'^[A-Za-z ]*$')

# model manager and validators 
class SubjectManager(models.Manager):
    def validate_subject_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['title']) < 3:
            errors.append("Subject must be at least 3 characters long")

        if not re.match(NAME_REGEX, post_data['title']):
            errors.append('Subject may only contain characters')

        # does this title already exist?
        subjects = Subject.objects.filter(title = post_data['title'])
        if len(subjects) > 0:
            errors.append('This subject title is already in use. Please choose a new title.')

        if len(post_data['description']) < 3:
            errors.append("Description must be at least 3 characters long")

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            this_user = User.objects.get(id=post_data['user_id'])

            subject = Subject.objects.create(
                title       = post_data['title'],
                description = post_data['description'],
                created_by  = this_user)
            
            subject.editors.add(this_user)

            response['subject'] = subject
            
        return response

class CardManager(models.Manager):
    def validate_card_data(self, request):
        response = {
            'status' : True
        }
        errors = []

        if len(request.POST['question']) < 3:
            errors.append("Question must be at least 3 characters long")

        if len(request.POST['answer']) < 3:
            errors.append("Answer must be at least 3 characters long")

        # does this question already exist?
        cards = Card.objects.filter(question = request.POST['question'])
        if len(cards) > 0:
            errors.append('This question is already in use. Please choose a new title.')

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            subject_id = int(request.POST['subject_id'])
            this_subject = Subject.objects.get(id=subject_id)

            card = Card.objects.create(
                question    = request.POST['question'],
                answer      = request.POST['answer'],
                hint        = request.POST['hint'],
                img         = request.FILES['this_file'],
                subject     = this_subject)
        
            response['card'] = card

        return response

# Models
class Subject(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField()
    created_by  = models.ForeignKey(User,related_name="subjects_created")
    editors     = models.ManyToManyField(User,related_name="subjects_editing")
    learners    = models.ManyToManyField(User,related_name="subjects_studying")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = SubjectManager()

class Card(models.Model):
    question    = models.TextField()
    answer      = models.TextField()
    hint        = models.TextField(default="")
    img         = models.ImageField(upload_to='images/')
    subject     = models.ForeignKey(Subject,related_name="cards")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = CardManager()
    


