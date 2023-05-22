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
    # context = {'is_auth': False,
    #            'page_obj': get_paginator(request, models.get_questions(models.new_questions))}
    context = {'is_auth': False,
               'page_obj': get_paginator(request, models.Question.objects.order_by_date())}

    if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
        return HttpResponseNotFound()
    return render(request, 'index.html', context)


def question(request, question_id: int):
    if (not models.Question.objects.filter(id=question_id).exists()) or question_id < 0:
        return HttpResponseNotFound()

    try:
        question_item = models.Question.objects.get_by_id(question_id)
        context = {'question': question_item,
                   'page_obj': get_paginator(request, models.Answer.objects.get_answers(question_item))}
    except (models.Question.DoesNotExist, models.Question.MultipleObjectsReturned):
        return HttpResponseNotFound()

    return render(request, 'question.html', context=context)


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    context = {'page_obj': get_paginator(request, models.Question.objects.order_by_rating())}

    if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
        return HttpResponseNotFound()

    return render(request, 'hot.html', context)


def tag(request, tag_name: str):
    current_tag = models.Tag.objects.filter(name=tag_name)
    if not current_tag.exists():
        return HttpResponseNotFound()

    context = {'page_obj': get_paginator(request, models.Question.objects.get_by_tag(tag_name)),
               'tag_name': tag_name}
    return render(request, "tag.html", context=context)

# def tag(request, tag_id: int):
#     # if not models.Tag.objects.filter(name=tag_name).exists():
#     #     return render(request, "page404.html", status=404)
#
#     try:
#         context = {'page_obj': get_paginator(request, models.get_questions(models.tag_questions, tag_id)),
#                    'tag_name': models.Tag.objects.get(id=tag_id).name}
#     except (models.Tag.DoesNotExist, models.Tag.MultipleObjectsReturned):
#         return HttpResponseNotFound()
#
#     context['tag_count'] = context['page_obj'].paginator.count
#
#     if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
#         return HttpResponseNotFound()
#
#     return render(request, 'tag.html', context)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
