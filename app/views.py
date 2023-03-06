from django.shortcuts import render
from . import models


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    return render(request, 'question.html')


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


