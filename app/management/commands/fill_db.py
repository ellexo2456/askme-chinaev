from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app import models


class Command(BaseCommand):
    help = 'Fill the database'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']

        models.Profile.objects.bulk_create(models.Profile for _ in range(ratio))

        models.Profile.objects.bulk_create(models.Profile(text=) for _ in range(ratio))


