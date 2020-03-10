from django.core.management.base import BaseCommand
from backend.seminars.models import Seminar


class Command(BaseCommand):
    help = "Checks the Seminars for actions to do"

    def handle(self, *args, **options):
        # expired = Seminar.objects.annotate_deadline_status().filter(
        #     deadline_status="expired"
        # )
        self.stdout.write("Not Implemented")
