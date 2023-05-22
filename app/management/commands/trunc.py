from app.models import Profile, Question, Answer, Tag, AnswerLike, QuestionLike

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core import management


class Command(BaseCommand):
    help = 'Fill the database'

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Profile, Question, Answer, Tag, AnswerLike, QuestionLike]
        for m in models:
            m.objects.all().delete()
