from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import models


def index(request):
    paginator = Paginator(models.QUESTIONS, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'is_auth': False, 'page_obj': page_obj}
    return render(request, 'index.html', context)


def question(request, question_id: int):
    if len(models.QUESTIONS) < question_id:
        return HttpResponseNotFound()
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
