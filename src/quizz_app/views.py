from django.shortcuts import render

from .models import Quiz, Question, Answer

# Create your views here.

def index(request):
    return render(request, 'index.html')