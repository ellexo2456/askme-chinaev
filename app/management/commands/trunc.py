from app.models import Profile, Question, Answer, Tag, Like

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core import management


class Command(BaseCommand):
    help = 'Fill the database'

    @transaction.atomic
    def handle(self, *args, **options):
        models = [Profile, Question, Answer, Tag, Like]
        for m in models:
            m.objects.all().delete()

        management.call_command('sqlsequencereset', app_label='app',
                                stdout=management.call_command('dbshell'))
