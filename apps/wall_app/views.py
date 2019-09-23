from django.shortcuts import render, redirect, HttpResponse
from .models import User

def index(request):
    return render(request, 'index.html')
