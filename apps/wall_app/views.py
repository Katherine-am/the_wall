from django.shortcuts import render, redirect, HttpResponse
from .models import User, Message, Comment
import bcrypt
from django.contrib import messages


def loginHomepage(request):
    return render(request, 'wall_app/loginHomepage.html')

def registration(request):

    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall_app')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)

    request.session['user_id'] = user.id

    return redirect('/wall_app/success')

def login(request):

    errors = User.objects.login_validator(request.POST)
    user = User.objects.filter(email=request.POST['email'])
    logged_user = user[0]

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall_app')
    
    else:
        request.session['user_id'] = logged_user.id

    return redirect('/wall_app/success')


def successfulLogin(request):

    if "user_id" not in request.session:
        return redirect('/wall_app')

    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "all_messages" : Message.objects.all()
    }
    
    return render(request, 'wall_app/wallHomepage.html', context)


def wallHomepage(request):

    if "user_id" not in request.session:
        return redirect('/wall_app')

    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "all_messages" : Message.objects.all()
    }

    return render(request, 'wall_app/wallHomepage.html', context)


def postMessage(request):

    errors = User.objects.message_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall_app/wall_homepage')
    else:
        Message.objects.create(message=request.POST['message'], user_id_id=request.session['user_id'])

    return redirect('wallHomepage')

def postComment(request):

    errors = User.objects.comment_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall_app/wall_homepage')
    else:
        Comment.objects.create(comment=request.POST['comment'], user_id_id=request.session['user_id'], message_id_id=request.POST['message_id'])
    
    return redirect('wallHomepage')


def logout(request):
    request.session.clear()
    return redirect('/wall_app')