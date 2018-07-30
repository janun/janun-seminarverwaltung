"""
TODOS:
 * moderation
 * User roles (ok?)
 * permission checking on transitions
 * Gruppenhut vs. Mitglied
 * colors for states? / Object for choices?
"""

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields.ranges import IntegerRangeField

from django_fsm import FSMField, transition
import rules
from model_utils.models import TimeStampedModel
from model_utils import Choices

from janun_seminarverwaltung.users.models import is_verwalter, is_teamer


def calc_max_funding(days, attendees, has_group):
    if days == 1:
        rate = 6.5
    elif has_group:
        rate = 11.5
    else:
        rate = 9.0
    return attendees * days * rate


class SeminarQuerySet(models.QuerySet):
    def by_quarter(self, quarter):
        if quarter == 1:
            return self.filter(start__month__in=(1, 2, 3))
        if quarter == 2:
            return self.filter(start__month__in=(4, 5, 6))
        if quarter == 3:
            return self.filter(start__month__in=(7, 8, 9))
        if quarter == 4:
            return self.filter(start__month__in=(10, 11, 12))
        return self

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

    title = models.CharField("Titel", max_length=255)
    content = models.TextField(
        "Inhalt",
        help_text="Welche Inhalte werden in Deinem Seminar vermittelt?",
    )
    start = models.DateTimeField("Startzeit")
    end = models.DateTimeField("Endzeit")
    location = models.CharField("Ort", max_length=255)
    planned_training_days = models.PositiveSmallIntegerField("Anzahl Bildungstage")
    planned_attendees = IntegerRangeField("Anzahl Teilnehmende")
    requested_funding = models.DecimalField("Benötigte Förderung", max_digits=6, decimal_places=2)
    group = models.ForeignKey(
        'groups.JANUNGroup',
        related_name="seminars",
        verbose_name="Gruppe",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    # ManyToManyField?? Damit mehrere Teamer author sein können?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="seminars",
        verbose_name="Autor_in",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    state = FSMField(
        default='angemeldet',
        # protected=True,
        choices=STATUS,
        verbose_name="Status"
    )

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


rules.add_perm('seminars.can_see_all_seminars', is_verwalter)
rules.add_perm('seminars.detail_seminar', is_verwalter | is_seminar_author | has_group_hat_for_seminar)
rules.add_perm('seminars.add_seminar', is_verwalter | is_teamer)
rules.add_perm('seminars.change_seminar', is_verwalter | is_seminar_author | has_group_hat_for_seminar)
rules.add_perm('seminars.delete_seminar', is_verwalter)
