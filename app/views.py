from django.shortcuts import render
from . import models


def index(request):
    context = {'questions': models.QUESTIONS, 'is_auth': False}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    context = {
        'answers': models.ANSWERS,
        'question': models.QUESTIONS[question_id - 1]
    }
    return render(request, 'question.html', context=context)


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'hot.html', context=context)


def tag(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'tag.html', context=context)


def ask(request):
    return render(request, 'ask.html')


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
