from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re
import bcrypt
from django.shortcuts import redirect

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"

        #email validation check
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"

        if User.objects.filter(email=postData['email']):
            errors["email"] = "User already exists"

        if len(postData['password']) < 6:
            errors["password"] = "Password must contain more than 6 characters"

        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords do not match"

        return errors
    
    def login_validator(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0]

            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()): 
                errors['password'] = "Email/password combination invalid"
        else:
            errors["email"] = "User does not exist"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, related_name="message")

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message_id = models.ForeignKey(Message, related_name="comment")
    user_id = models.ForeignKey(User, related_name="comment")


