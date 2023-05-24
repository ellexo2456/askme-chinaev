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


def add_tags_to_question(tags, question):
    for tag_name in tags.split(','):
        tag = models.Tag(name=tag_name)
        try:
            tag.save()
            question.tags.add(tag)
        except IntegrityError:
            pass


def paginate(request, page_items):
    paginator = Paginator(page_items, ITEMS_COUNT_ON_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def get_num_page_by_id(paginator, id):
    for i in paginator.page_range:
        entities = paginator.page(i).object_list
        for entity in entities.all():
            if entity.id == id:
                return i
    return None


def index(request):
    # context = {'is_auth': False,
    #            'page_obj': get_paginator(request, models.get_questions(models.new_questions))}
    context = {'is_auth': True,
               'page_obj': paginate(request, models.Question.objects.order_by_date())}

    if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
        return HttpResponseNotFound()
    return render(request, 'index.html', context)


def question(request, question_id: int):
    needed_question = models.Question.objects.filter(pk=question_id).first()

    if not needed_question:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    if request.method == 'GET':
        answer_form = forms.AnswerForm()
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect("login")
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)

            user = models.User.objects.get(username=request.user)
            answer.profile = models.Profile.objects.get(user=user)

            answer.question = needed_question
            answer.save()
            answer_id = answer.id

            # дублирование, т.к. при GET запросе новый ответ не добавляется
            # answers = needed_question.answer_set.all().order_by('date')
            answers = needed_question.answers.order_by('-rating')
            page = paginate(request, answers)

            # получаем номер страницы, на которой разместился новый вопрос
            num_page = get_num_page_by_id(page.paginator, answer_id)
            # скроллинг по якорю: <div id="{{answer_id"}}"> </div>
            return redirect(reverse("question", args=[question_id]) + f'?page={num_page}#{answer_id}')

    answers = needed_question.answers.order_by('-rating')
    page = paginate(request, answers)
    context = {'page_obj': page, 'question': needed_question, 'form': answer_form}
    return render(request, "question.html", context=context)


def hot(request):
    context = {'page_obj': paginate(request, models.Question.objects.order_by_rating())}

    if request.GET.get('page') and int(request.GET.get('page')) > context['page_obj'].paginator.num_pages:
        return HttpResponseNotFound()

    return render(request, 'hot.html', context)


def tag(request, tag_name: str):
    current_tag = models.Tag.objects.filter(name=tag_name)
    if not current_tag.exists():
        return HttpResponseNotFound()

    context = {'page_obj': paginate(request, models.Question.objects.get_by_tag(tag_name)),
               'tag_name': tag_name}
    return render(request, "tag.html", context=context)


@login_required(login_url="login", redirect_field_name=settings.REDIRECT_FIELD_NAME)
def ask(request):
    if request.method == 'GET':
        ask_form = forms.AskForm()
    elif request.method == 'POST':
        ask_form = forms.AskForm(request.POST)
        if ask_form.is_valid():
            question = ask_form.save(commit=False)
            user = models.User.objects.get(username=request.user)
            question.profile = models.Profile.objects.get(user=user)
            question.save()
            add_tags_to_question(ask_form.cleaned_data['tag_list'], question)
            return redirect(reverse("question", args=[question.id]))

    context = {'form': ask_form}
    return render(request, "ask.html", context=context)


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


def logout(request):
    auth.logout(request)
    return redirect(request.META['HTTP_REFERER'])


def register(request):
    if request.method == 'GET':
        reg_form = forms.RegistrationForm()
    elif request.method == 'POST':
        reg_form = forms.RegistrationForm(data=request.POST, files=request.FILES)
        if reg_form.is_valid():
            user = reg_form.save()
            if user:
                # avatar = None ?
                auth.login(request, user)
                models.Profile.objects.create(user=user, avatar=reg_form.cleaned_data['avatar'])
                return redirect(reverse(viewname="index"))
            else:
                reg_form.add_error(None, "User saving error")
    context = {'form': reg_form}
    return render(request, "register.html", context=context)


@login_required(login_url="login", redirect_field_name=settings.REDIRECT_FIELD_NAME)
def settings(request):
    if request.method == 'GET':
        dict_model_fields = model_to_dict(request.user)
        # инициализация формы существующими значениями
        user_form = forms.SettingsForm(initial=dict_model_fields)
    elif request.method == 'POST':
        user_form = forms.SettingsForm(data=request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse("settings"))
    context = {'form': user_form}
    return render(request, "settings.html", context=context)
