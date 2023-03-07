from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import models


def get_paginator(request, page_items):
    paginator = Paginator(page_items, 10)

    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    context = {'is_auth': False, 'page_obj': get_paginator(request, models.QUESTIONS)}
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
    return render(request, 'hot.html', {'page_obj': get_paginator(request, models.QUESTIONS)})


def tag(request):
    return render(request, 'tag.html', {'page_obj': get_paginator(request, models.QUESTIONS)})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
