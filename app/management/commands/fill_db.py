from app.models import Profile, Question, Answer, Tag, AnswerLike, QuestionLike, User

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app.management.commands._factories import (
    TagFactory,
    QuestionFactory,
    ProfileFactory,
    AnswerFactory,
    QuestionLikeFactory,
    AnswerLikeFactory
)

import random


class Command(BaseCommand):
    help = 'Fill the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=10000)

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Profile, Question, Answer, Tag, AnswerLike, QuestionLike, User]
        for m in models:
            m.objects.all().delete()

        ratio = options['ratio']

        users = []
        for i in range(ratio):
            user = User(username=f'username{i}')
            user.set_password('tr12345')
            users.append(user)
        User.objects.bulk_create(users)

        profiles = Profile.objects.bulk_create(ProfileFactory(user=users[i]) for i in range(ratio))

        tags = Tag.objects.bulk_create(TagFactory() for _ in range(ratio))

        questions = []
        for _ in range(ratio * 10):
            question = QuestionFactory.create(profile=random.choice(profiles),
                                              tags=random.choices(tags, k=random.choice([1, 2, 3])))
            questions.append(question)

        answers = [AnswerFactory(
            profile=random.choice(profiles),
            question=random.choice(questions)
        ) for _ in range(ratio * 100)]
        Answer.objects.bulk_create(answers)

        answers_likes = []
        for _ in range(ratio * 100):
            answer_like = AnswerLikeFactory(
                profile=random.choice(profiles),
                answer=random.choice(answers)
            )
            answers_likes.append(answer_like)
        AnswerLike.objects.bulk_create(answers_likes)

        questions_likes = []
        for _ in range(ratio * 100):
            question_like = QuestionLikeFactory(
                profile=random.choice(profiles),
                question=random.choice(questions)
            )
            questions_likes.append(question_like)
        QuestionLike.objects.bulk_create(questions_likes)
