import factory
from factory.django import DjangoModelFactory
from app import models


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = models.Profile


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = models.Question

    title = factory.Faker('text', max_nb_chars=60)
    text = factory.Faker('text')
    ask_date = factory.Faker('date_this_year')
    correct_answer = factory.SubFactory('AnswerFactory', question=)
    profile = factory.SubFactory(ProfileFactory)



class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = models.Answer

    text = factory.Faker('text')
    ask_date = factory.Faker('date_this_year')
    profile = factory.SubFactory(ProfileFactory)
    question = factory.SubFactory(QuestionFactory)

