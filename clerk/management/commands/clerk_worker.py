from django.core.management.base import BaseCommand, CommandError
from ...models import Contest


class Command(BaseCommand):
    help = 'Runs clerk routine'

    def handle(self, *args, **options):
        try:
            while True:
                for contest in Contest.objects.all():
                    contest.pull_new_submissions()
        except InterruptedError:
            pass