from django.core.paginator import Paginator

from django.conf import Settings
from django.db import IntegrityError
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from app import forms
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from . import models
from askme import settings

ITEMS_COUNT_ON_PAGE = 10


def get_paginator(request, page_items):
    paginator = Paginator(page_items, ITEMS_COUNT_ON_PAGE)

    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@login_required(login_url="login")
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


@login_required(login_url="login", redirect_field_name=settings.REDIRECT_FIELD_NAME)
def ask(request):
    return render(request, 'ask.html')


# def login(request):
#     return render(request, 'login.html')


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("request.GET 1 = ", request.GET)
            url = request.GET.get('continue', '/')
            # if not url:
            #     url = '/'
            return HttpResponseRedirect(url)
        login_form = forms.LoginForm()
        print("request.GET 2 = ", request.GET)
    elif request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                print("request.POST = ", request.POST)
                print("request.POST_GET = ", request.GET)
                # return HttpResponseRedirect(reverse(viewname="register", kwargs={'continue' : '/'}))

                return redirect(reverse(viewname="login") + "?continue=" + request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Username or password is incorrect")
    # context = {'best_items': get_best_items(), 'form': login_form}
    context = {'form': login_form}

    return render(request, "login.html", context=context)



def register(request):
    return render(request, 'register.html')


@login_required(login_url="login", redirect_field_name=settings.REDIRECT_FIELD_NAME)
def settings(request):
    return render(request, 'settings.html')
