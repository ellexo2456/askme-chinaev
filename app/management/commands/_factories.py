import factory
from factory.django import DjangoModelFactory
from app import models

import random


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = models.Profile
        strategy = factory.BUILD_STRATEGY

    avatar = factory.django.ImageField(from_path='static/img/avatar-3.jpg')


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = models.Question
        strategy = factory.BUILD_STRATEGY

    title = factory.Faker('text', max_nb_chars=60)
    text = factory.Faker('text')
    profile = factory.SubFactory(ProfileFactory)
    answers_count = factory.Faker('random_int', max=100)
    rating = factory.Faker('random_int', max=100)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        try:
            self.tags.add(*extracted)
        except ValueError:
            print("Can`t fill ManyToMany rel Question-Tag")


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = models.Answer
        strategy = factory.BUILD_STRATEGY

    text = factory.Faker('text')
    profile = factory.SubFactory(ProfileFactory)
    question = factory.SubFactory(QuestionFactory)
    rating = factory.Faker('random_int', max=100)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = models.Tag
        strategy = factory.BUILD_STRATEGY

    name = factory.Faker('word')
    count = factory.Faker('random_int', max=100)


class QuestionLikeFactory(DjangoModelFactory):
    class Meta:
        model = models.QuestionLike
        strategy = factory.BUILD_STRATEGY

    question = factory.SubFactory(QuestionFactory)
    profile = factory.SubFactory(ProfileFactory)
    is_like = factory.Faker('boolean')


class AnswerLikeFactory(DjangoModelFactory):
    class Meta:
        model = models.AnswerLike
        strategy = factory.BUILD_STRATEGY

    answer = factory.SubFactory(AnswerFactory)
    profile = factory.SubFactory(ProfileFactory)
    is_like = factory.Faker('boolean')

