from django.core.management.base import BaseCommand
from django.utils import timezone

from backend.seminars.models import Seminar, SeminarCheck
from backend.emails.models import EmailTemplate


class Command(BaseCommand):
    help = "Checks the Seminars for actions to do"

    def check_deadline_expired(self):
        """Check for seminars with deadline_status expired"""
        expired = (
            Seminar.objects.annotate_deadline_status()
            .filter(deadline_status="expired")
            .exclude(checks__check_type="deadline_expired")
        )
        for seminar in expired:
            EmailTemplate.send("seminar_deadline_expired", {"seminar": seminar})
            SeminarCheck.objects.create(seminar=seminar, check_type="deadline_expired")

    def check_deadline_soon(self):
        """Check for seminars with deadline_status soon"""
        expired = (
            Seminar.objects.annotate_deadline_status()
            .filter(deadline_status="soon")
            .exclude(checks__check_type="deadline_soon")
        )
        for seminar in expired:
            EmailTemplate.send("seminar_deadline_soon", {"seminar": seminar})
            SeminarCheck.objects.create(seminar=seminar, check_type="deadline_soon")

    def check_seminar_occurred(self):
        """Check for seminars with end_date in the past"""
        expired = (
            Seminar.objects.annotate_deadline_status()
            .filter(end_date__gte=timezone.now())
            .exclude(checks__check_type="occurred")
        )
        for seminar in expired:
            EmailTemplate.send("seminar_occurred", {"seminar": seminar})
            SeminarCheck.objects.create(seminar=seminar, check_type="occurred")

    def handle(self, *args, **options):
        self.check_deadline_expired()
        self.check_deadline_soon()
        self.check_seminar_occurred()
