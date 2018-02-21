from __future__ import unicode_literals

from django.db import models

import re
import bcrypt

NAME_REGEX = re.compile(r'^[A-Za-z ]*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# model manager and validators 
class UserManager(models.Manager):
    def validate_registration_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['first_name']) < 3:
            errors.append("First name must be at least 3 characters long")

        if not re.match(NAME_REGEX, post_data['first_name']):
            errors.append('First name may only contain characters')

        if len(post_data['last_name']) < 3:
            errors.append("Last name must be at least 3 characters long")

        if not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('Last name may only contain characters')

        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Invalid email")

        # does this email already exist?
        users = User.objects.filter(email = post_data['email'])
        if len(users) > 0:
            errors.append('This email is already in use')

        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters long")

        if post_data['password'] != post_data['pwd_confirm']:
            errors.append("Passwords do not match!")

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            user = User.objects.create(
                        email           = post_data['email'],
                        first_name      = post_data['first_name'],
                        last_name       = post_data['last_name'],
                        organization    = post_data['organization'],
                        password        = hashedpwd)

            response['user'] = user
            
        return response

    def validate_login_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

        user = User.objects.filter(email = post_data['email'])

        if len(user) > 0:
            # check this user's password
            user = user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username does not exist - please register')

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            response['user'] = user
        return response

# Models
class User(models.Model):
    email       = models.CharField(max_length=255)
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    organization= models.CharField(max_length=255,default="None")
    password    = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()

