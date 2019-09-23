from django.shortcuts import render, redirect, HttpResponse
from .models import User, Message, Comment

def index(request):
    return render(request, 'index.html')
