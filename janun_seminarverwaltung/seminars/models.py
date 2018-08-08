"""
TODOS:
 * moderation
 * User roles (ok?)
 * permission checking on transitions
 * Gruppenhut vs. Mitglied
 * colors for states? / Object for choices?
"""

from datetime import date, timedelta
import math

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields.ranges import IntegerRangeField
from django.core.exceptions import ValidationError
from django.utils.formats import date_format

from django_fsm import FSMField, transition
import rules
from model_utils.models import TimeStampedModel
from model_utils import Choices

from janun_seminarverwaltung.users.models import is_verwalter, is_teamer, is_pruefer


class SeminarQuerySet(models.QuerySet):
    def by_quarter(self, quarter):
        return self.filter(start__quarter=quarter)

    def by_year(self, year):
        return self.filter(start__year=year)


class Seminar(TimeStampedModel, models.Model):

    STATUS = Choices(
        ('ANGEMELDET', 'angemeldet'),
        ('ZURUECKGEZOGEN', 'zurückgezogen'),
        ('ZUGESAGT', 'zugesagt'),
        ('ABGELEHNT', 'abgelehnt'),
        ('ABGESAGT', 'abgesagt'),
        ('STATTGEFUNDEN', 'hat stattgefunden'),
        ('OHNE_ABRECHNUNG', 'ohne Abrechnung'),
        ('ABGESCHICKT', 'Abrechnung abgeschickt'),
        ('ANGEKOMMEN', 'Abrechnung angekommen'),
        ('UNMOEGLICH', 'Abrechnung unmöglich'),
        ('RECHNERISCH', 'rechn. Prüfung'),
        ('INHALTLICH', 'inhlt. Prüfung'),
        ('NACHPRUEFUNG', 'Nachprüfung'),
        ('FERTIG', 'fertig geprüft'),
        ('UEBERWIESEN', 'überwiesen'),
    )

    title = models.CharField("Titel", max_length=255, unique_for_date="start")
    content = models.TextField(
        "Inhalt",
        help_text="Welche Inhalte werden in Deinem Seminar vermittelt?",
    )
    start = models.DateTimeField("Startzeit")
    end = models.DateTimeField("Endzeit")
    location = models.CharField("Ort", max_length=255)
    planned_training_days = models.PositiveSmallIntegerField("Anzahl Bildungstage")
    planned_attendees = IntegerRangeField("Anzahl Teilnehmende")
    requested_funding = models.DecimalField("Benötigte Förderung", max_digits=10, decimal_places=2)
    group = models.ForeignKey(
        'groups.JANUNGroup',
        related_name="seminars",
        verbose_name="Gruppe",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    # QUESTION: ManyToManyField?? Damit mehrere Teamer author sein können?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="seminars",
        verbose_name="Autor_in",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    state = FSMField(
        default='ANGEMELDET',
        # protected=True,
        choices=STATUS,
        verbose_name="Status"
    )
    mobility_barriers = models.TextField(
        "Moblitäts-Barrieren",
        help_text="Zum Bsp.: Müssen Stufen oder Treppen überwunden werden?"
                  "Findet ein Workshop im Garten statt? Sind sportliche Betätigungen vorgesehen?",
        blank=True,
        null=True,
    )
    language_barriers = models.TextField(
        "Sprach-Barrieren",
        help_text="Zum Bsp.: Kommen viele Fachausdrücke vor?"
                  "Sind die Workshops auch für Menschen geeignet, die wenig Deutsch sprechen?",
        blank=True,
        null=True,
    )
    hearing_barriers = models.TextField(
        "Hör-Barrieren",
        help_text="Zum Bsp.: Werden Filme mit oder ohne Untertitel gezeigt?"
                  "Sind laute (Stör-)Geräusche wahrscheinlich?",
        blank=True,
        null=True,
    )
    seeing_barriers = models.TextField(
        "Seh-Barrieren",
        help_text="Zum Bsp.: Findet Textarbeit statt? Muss man Farben erkennen können?",
        blank=True,
        null=True,
    )

    @property
    def planned_tnt(self):
        if self.planned_attendees and self.planned_training_days:
            return self.planned_attendees.upper * self.planned_training_days
        return None

    def get_max_funding(self):
        if not self.planned_tnt:
            return None
        # calc rate
        if self.planned_training_days == 1:
            rate = 6.5
        elif self.group:
            rate = 11.5
        else:
            rate = 9.0
        # tnt * rate
        funding = self.planned_tnt * rate

        if self.group:
            return funding

        if self.planned_training_days <= 3:
            limit = 300
        else:
            limit = 300 + 200 * (self.planned_training_days - 3)
        if limit > 1000:
            limit = 1000

        if funding > limit:
            return limit
        return funding

    def get_deadline(self):
        if not self.end:
            return None
        year = self.end.year
        deadlines = {
            1: date(year, 4, 15),
            2: date(year, 7, 15),
            3: date(year, 10, 15),
            4: date(year, 1, 15)
        }
        quarter = math.ceil(self.end.month / 3)
        return deadlines[quarter]

    def get_duration(self):
        if self.end and self.start and self.end > self.start:
            return (self.end - self.start).days + 1
        return None

    def clean_title(self):
        if self.start and self.title:
            qs = Seminar.objects.filter(start__date=self.start.date())
            qs.filter(title=self.title)
            if self.pk:
                qs.exclude(pk=self.pk)
            if qs.exists():
                return ValidationError(
                    "Es existiert schon ein Seminar mit diesem Titel und Startzeitpunkt am %(date)s.",
                    params={'title': self.title, 'date': date_format(self.start)}
                )
        return None

    def clean_end(self):
        if self.end and self.start:
            if self.end < self.start:
                return ValidationError("Endzeit muss nach Startzeit liegen.")
        return None

    def clean_planned_training_days(self):
        if self.planned_training_days:
            max_days = self.get_duration()
            if max_days and self.planned_training_days > max_days:
                return ValidationError(
                    "Darf nicht größer sein, als die Dauer Deines Seminars (%(days)s Tage).",
                    params={'days': max_days}
                )
        return None

    def clean_requested_funding(self):
        if self.requested_funding:
            max_funding = self.get_max_funding()
            if max_funding and self.requested_funding > max_funding:
                return ValidationError(
                    "Sorry, die maximale Förderung für Dein Seminar beträgt %(max_funding).2f €.",
                    params={'max_funding': max_funding}
                )
        return None

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        fields = ('title', 'end', 'planned_training_days', 'requested_funding')
        errors = {}
        for field in fields:
            if not exclude or field not in exclude:
                error = getattr(self, 'clean_%s' % field)()
                if error:
                    errors[field] = error
        if errors:
            raise ValidationError(errors)

    objects = SeminarQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('seminars:detail', args=[self.pk])

    class Meta:
        ordering = ["start"]
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"
        permissions = (
            ('detail_seminars', "Kann Seminardaten sehen"),
            ('can_see_all_seminars', "Kann alle Seminare sehen")
        )

    def __str__(self):
        return self.title

    def is_in_the_past(self):
        return timezone.now() > self.end

    @transition(field=state,
                source=['ANGEMELDET', 'ABGELEHNT', 'ABGESAGT'],
                target='ZUGESAGT',
                custom=dict(button_name="Zusagen"))
    def zusagen(self):
        pass

    @transition(field=state,
                source=['ZUGESAGT'],
                target='ABGESAGT',
                custom=dict(button_name="Absagen"))
    def absagen(self):
        pass

    @transition(field=state,
                source=['ANGEMELDET', 'ZUGESAGT'],
                target='ABGELEHNT',
                custom=dict(button_name="Ablehnen"))
    def ablehnen(self):
        pass

    @transition(field=state,
                source=['ANGEMELDET', 'ZUGESAGT'],
                target='ZURUECKGEZOGEN',
                custom=dict(button_name="Zurückziehen"))
    def zurueckziehen(self):
        pass

    @transition(field=state,
                source=['ZUGESAGT'],
                target='STATTGEFUNDEN',
                custom=dict(button_name="Stattfinden bestätigen"),
                conditions=[is_in_the_past])
    def stattfinden(self):
        pass

    @transition(field=state,
                source=['STATTGEFUNDEN'],
                target='OHNE_ABRECHNUNG',
                custom=dict(button_name="ohne Abrechnung"))
    def ohne_abrechnung(self):
        pass

    @transition(field=state,
                source=['STATTGEFUNDEN'],
                target='ABGESCHICKT',
                custom=dict(button_name="Abrechnung abgeschickt bestätigen"))
    def abschicken(self):
        pass

    @transition(field=state,
                source=['STATTGEFUNDEN', 'ABGESCHICKT'],
                target='ANGEKOMMEN',
                custom=dict(button_name="Abrechnung angekommen bestätigen"))
    def ankommen(self):
        pass

    @transition(field=state,
                source=['ANGEKOMMEN'],
                target='RECHNERISCH',
                custom=dict(button_name="in die rechnerische Prüfung"))
    def rechnen(self):
        pass

    @transition(field=state,
                source=['RECHNERISCH'],
                target='INHALTLICH',
                custom=dict(button_name="in die inhaltliche Prüfung"))
    def inhalten(self):
        pass

    @transition(field=state,
                source=['INHALTLICH'],
                target='NACHPRUEFUNG',
                custom=dict(button_name="in die Nachprüfung"))
    def nach_pruefen(self):
        pass

    @transition(field=state,
                source=['NACHPRUEFUNG'],
                target='FERTIG',
                custom=dict(button_name="Prüfung abschließen"))
    def fertigen(self):
        pass

    @transition(field=state,
                source=['FERTIG'],
                target='UEBERWIESEN',
                custom=dict(button_name="Überweisung bestätigen"))
    def ueberweisen(self):
        pass

    @transition(field=state,
                source=['NACHPRUEFUNG', 'INHALTLICH', 'ANGEKOMMEN'],
                target='UNMOEGLICH',
                custom=dict(button_name="Abrechnung unmöglich"))
    def unmoeglichen(self):
        pass


@rules.predicate
def is_seminar_author(user, seminar):
    return seminar.author == user


@rules.predicate
def has_group_hat_for_seminar(user, seminar):
    return seminar.group in user.group_hats.all()


@rules.predicate
def just_created(user, seminar):
    return seminar.created > (timezone.now() - timedelta(minutes=5))


rules.add_perm('seminars.can_see_all_seminars', is_verwalter)
rules.add_perm('seminars.detail_seminar', is_verwalter | is_seminar_author | has_group_hat_for_seminar)
rules.add_perm('seminars.add_seminar', is_verwalter | is_teamer)
rules.add_perm('seminars.change_seminar', is_verwalter | is_seminar_author | has_group_hat_for_seminar)
rules.add_perm('seminars.delete_seminar', is_verwalter | is_seminar_author & just_created)
