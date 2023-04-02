from app.models import Profile, Question, Answer, Tag, Like

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from _factories import (
    TagFactory,
    ProfileFactory,
    QuestionFactory,
    AnswerFactory,
    LikeFactory
)

import random


class Command(BaseCommand):
    help = 'Fill the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=10000)

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Profile, Question, Answer, Tag, Like]
        for m in models:
            m.objects.all().delete()

        ratio = options['ratio']

        profiles = [Profile() for _ in range(ratio)]
        Profile.objects.bulk_create(profiles)

        tags = [TagFactory for _ in range(ratio)]
        Tag.objects.bulk_create(tags)

        questions = []
        for _ in range(ratio * 10):
            question = QuestionFactory(profile=random.choices(profiles))
            question.tags(random.choices(tags, k=random.choice([1, 2, 3])))
            questions.append(question)
        Question.objects.bulk_create(questions)

        answers = [AnswerFactory(
            profile=random.choice(profiles),
            question=random.choice(questions)
        ) for _ in range(ratio * 100)]
        Answer.objects.bulk_create(answers)

        likes = []
        for _ in range(ratio * 200):
            flag = random.choice([True, False])
            like = LikeFactory(
                profile=random.choice(profiles),
                question=random.choice(questions) if flag else None,
                answer=random.choice(answers) if not flag else None
            )
            likes.append(like)
        Like.objects.bulk_create(likes)

