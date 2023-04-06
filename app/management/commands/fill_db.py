from app.models import Profile, Question, Answer, Tag, Like

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app.management.commands._factories import (
    TagFactory,
    QuestionFactory,
    ProfileFactory,
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

        profiles = Profile.objects.bulk_create(ProfileFactory() for _ in range(ratio))

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
