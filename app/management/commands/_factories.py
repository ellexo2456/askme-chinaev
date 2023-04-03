import factory
from factory.django import DjangoModelFactory
from app import models

import random


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = models.Profile
        strategy = factory.BUILD_STRATEGY


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = models.Question
        strategy = factory.BUILD_STRATEGY

    title = factory.Faker('text', max_nb_chars=60)
    text = factory.Faker('text')
    # ask_date = factory.Faker('date_this_year')
    profile = factory.SubFactory(ProfileFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tags.add(*extracted)


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = models.Answer
        strategy = factory.BUILD_STRATEGY

    text = factory.Faker('text')
    # ask_date = factory.Faker('date_this_year')
    profile = factory.SubFactory(ProfileFactory)
    question = factory.SubFactory(QuestionFactory)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = models.Tag
        strategy = factory.BUILD_STRATEGY

    name = factory.Faker('word')


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = models.Like
        strategy = factory.BUILD_STRATEGY

    estimation = random.choice(['L', 'D'])
    question = factory.SubFactory(QuestionFactory)
    answer = factory.SubFactory(AnswerFactory)
    profile = factory.SubFactory(ProfileFactory)
