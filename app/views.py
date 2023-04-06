from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import models

ITEMS_COUNT_ON_PAGE = 10


def get_paginator(request, page_items):
    paginator = Paginator(page_items, ITEMS_COUNT_ON_PAGE)

    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    context = {'is_auth': False,
               'page_obj': get_paginator(request, models.get_questions(models.new_questions))}
    if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
        return HttpResponseNotFound()
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
    context = {'page_obj': get_paginator(request, models.QUESTIONS)}
    if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
        return HttpResponseNotFound()
    return render(request, 'hot.html', context)


def tag(request, tag_id: int):
    context = {'page_obj': get_paginator(request, models.get_questions(models.tag_questions, tag_id)),
               'tag_name': models.Tag.objects.get(id=tag_id).name}

    if context['page_obj'].paginator.count == 0:
        return HttpResponseNotFound()

    context['tag_count'] = context['page_obj'].paginator.count

    if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
        return HttpResponseNotFound()

    return render(request, 'tag.html', context)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
