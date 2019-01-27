"""
TODOS:
 * moderation
 * User roles (ok?)
 * permission checking on transitions
 * Gruppenhut vs. Mitglied
 * colors for states? / Object for choices?
"""

from datetime import date, timedelta, datetime
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

from janun_seminarverwaltung.users.models import is_verwalter, is_teamer, is_pruefer, is_reviewed


class SeminarQuerySet(models.QuerySet):
    def by_quarter(self, quarter):
        return self.filter(start_date__quarter=quarter)

    def by_year(self, year):
        return self.filter(start_date__year=year)

    def this_year(self):
        return self.by_year(timezone.now().year)


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

    def get_state_color(self):
        if self.state in ('ZURUECKGEZOGEN', 'ABGELEHNT', 'ABGESAGT', 'OHNE_ABRECHNUNG', 'UNMOEGLICH'):
            return 'danger'
        return 'primary'

    title = models.CharField(
        "Titel", max_length=255,
        help_text="Beschreibe oder benenne das Seminar in wenigen Worten"
    )
    content = models.TextField(
        "Inhalt",
        help_text="Um was genau geht es in dem Seminar?<br>Welche Inhalte werden vermittelt?",
    )
    start_date = models.DateField("Anfangsdatum")
    start_time = models.TimeField("Anfangszeit", blank=True, null=True)
    end_date = models.DateField("Enddatum")
    end_time = models.TimeField("Endzeit", blank=True, null=True)
    location = models.CharField(
        "Ort", max_length=255,
        help_text="Stadt, in der das Seminar stattfinden soll."
    )
    planned_training_days = models.PositiveSmallIntegerField("gepl. Bildungstage")
    planned_attendees_min = models.PositiveSmallIntegerField("Teilnehmende min.")
    planned_attendees_max = models.PositiveSmallIntegerField("Teilnehmende max.")
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
        verbose_name="Anmelder_in",
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

    ### Abrechnungsfelder:
    verwendungsnachweis = models.BooleanField(
        "Verwendungsnachweis",
        default=True,
        help_text="Soll das Seminar im Verwendungsnachweis auftauchen?"
    )

    tn_total = models.PositiveSmallIntegerField("TN insgesamt", blank=True, null=True)
    tn_jfg = models.PositiveSmallIntegerField("TN nach JFG", blank=True, null=True)

    tnt_total = models.PositiveSmallIntegerField("TNT nach RL", blank=True, null=True)
    tnt_jfg = models.PositiveSmallIntegerField("TNT nach JFG", blank=True, null=True)

    vorschuss = models.DecimalField("Vorschuss", max_digits=10, decimal_places=2, default=0)

    ausgaben_verpflegung = models.DecimalField("Verpflegung", max_digits=10, decimal_places=2, default=0)
    ausgaben_unterkunft = models.DecimalField("Unterkunft", max_digits=10, decimal_places=2, default=0)
    ausgaben_referenten = models.DecimalField("Referent_innen", max_digits=10, decimal_places=2, default=0)
    ausgaben_fahrtkosten = models.DecimalField("Fahrtkosten", max_digits=10, decimal_places=2, default=0)
    ausgaben_sonstiges = models.DecimalField("Sonstiges", max_digits=10, decimal_places=2, default=0)

    einnahmen_beitraege = models.DecimalField("TN-Beiträge", max_digits=10, decimal_places=2, default=0)
    einnahmen_oeffentlich = models.DecimalField("Öff. Zuwendg.", max_digits=10, decimal_places=2, default=0)
    einnahmen_sonstiges = models.DecimalField("Sonstiges", max_digits=10, decimal_places=2, blank=True, default=0)

    training_days = models.PositiveSmallIntegerField("tats. Bildungstage", blank=True, null=True)

    foerderbedarf = models.DecimalField("Förderbedarf", max_digits=10, decimal_places=2, blank=True, null=True)

    LANDKREISE = Choices(
        ('1', '1 Landkreis'),
        ('2', '2–3 Landkreisen'),
        ('4', '4 oder mehr Landkreisen'),
    )

    landkreise = models.CharField(
        verbose_name="TN-Landkreise",
        max_length=100,
        choices=LANDKREISE,
        blank=True,
    )

    ### website Felder:
    # (werden z.Z. noch nicht benutzt)

    mobility_barriers = models.TextField(
        "Mobilitäts-Barrieren",
        help_text="Zum Bsp.: Müssen Stufen oder Treppen überwunden werden? "
                  "Findet ein Workshop im Garten statt? Sind sportliche Betätigungen vorgesehen?",
        blank=True,
        null=True,
    )
    language_barriers = models.TextField(
        "Sprach-Barrieren",
        help_text="Zum Bsp.: Kommen viele Fachausdrücke vor? "
                  "Sind die Workshops auch für Menschen geeignet, die wenig Deutsch sprechen?",
        blank=True,
        null=True,
    )
    hearing_barriers = models.TextField(
        "Hör-Barrieren",
        help_text="Zum Bsp.: Werden Filme mit oder ohne Untertitel gezeigt? "
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
    def ausgaben_unterkunft_verpflegung(self):
        return self.ausgaben_unterkunft + self.ausgaben_verpflegung

    @property
    def ausgaben(self):
        return self.ausgaben_unterkunft + self.ausgaben_verpflegung + self.ausgaben_referenten + self.ausgaben_fahrtkosten + self.ausgaben_sonstiges

    @property
    def einnahmen(self):
        return self.einnahmen_beitraege + self.einnahmen_oeffentlich + self.einnahmen_sonstiges

    @property
    def ausgaben_minus_einnahmen(self):
        return self.ausgaben - self.einnahmen

    @property
    def resterstattung(self):
        if self.foerderbedarf:
            return self.foerderbedarf - self.vorschuss
        return None


    @property
    def start(self):
        if self.start_time:
            return datetime.combine(self.start_date, self.start_time)
        return self.start_date

    @property
    def end(self):
        if self.end_time:
            return datetime.combine(self.end_date, self.end_time)
        return self.end_date

    @property
    def tnt(self):
        if self.tnt_jfg:
            return self.tnt_jfg
        return self.planned_tnt

    @property
    def funding(self):
        if self.foerderbedarf:
            return self.foerderbedarf
        return self.max_funding

    @property
    def planned_tnt(self):
        if self.planned_attendees_max and self.planned_training_days:
            return self.planned_attendees_max * self.planned_training_days
        return 0

    @property
    def rate(self):
        if self.planned_training_days == 1:
            return 7.5
        if self.group:
            return 12.5
        return 9.0

    @property
    def max_funding(self):
        return self.get_max_funding(self.tnt_total)

    def get_max_funding(self, tnt=None):
        if tnt is None:
            tnt = self.planned_tnt
        if not tnt:
            return None
        funding = tnt * self.rate

        # no limit if group
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
        if not self.end_date:
            return None
        year = self.end_date.year
        deadlines = {
            1: date(year, 4, 15),
            2: date(year, 7, 15),
            3: date(year, 10, 15),
            4: date(year, 1, 15)
        }
        quarter = math.ceil(self.end_date.month / 3)
        return deadlines[quarter]

    def get_duration(self):
        if self.end_date and self.start_date:
            return (self.end_date - self.start_date).days + 1
        return None

    def clean_end_date(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                return ValidationError("Endzeit muss nach Startzeit liegen.")
        return None

    def clean_planned_training_days(self):
        if self.planned_training_days:
            max_days = self.get_duration()
            if max_days and self.planned_training_days > max_days:
                return ValidationError(
                    "Darf nicht größer sein, als die Dauer des Seminars (%(days)s Tage).",
                    params={'days': max_days}
                )
        return None

    def clean_requested_funding(self):
        if self.requested_funding:
            max_funding = self.get_max_funding()
            if max_funding and self.requested_funding > max_funding:
                return ValidationError(
                    "Sorry, die maximale Förderung für das Seminar beträgt %(max_funding)d €.",
                    params={'max_funding': max_funding}
                )
        return None

    def clean_planned_attendees_max(self):
        if self.planned_attendees_max and self.planned_attendees_min:
            if self.planned_attendees_min > self.planned_attendees_max:
                return ValidationError(
                    "Darf nicht kleiner sein als %(field)s",
                    params={'field': self._meta.get_field('planned_attendees_min').verbose_name}
                )
        return None

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        fields = ('end_date', 'planned_training_days', 'requested_funding', 'planned_attendees_max')
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
        ordering = ['start_date', 'start_time']
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"
        permissions = (
            ('detail_seminars', "Kann Seminardaten sehen"),
            ('can_see_all_seminars', "Kann alle Seminare sehen")
        )

    def __str__(self):
        return self.title

    def is_in_the_past(self):
        return timezone.now().date() > self.end_date

    # TODO: Wenn Abrechnungszeitraum abläuft, Erinnerungsmail an Autor schicken.
    # TODO: Wenn Seminar stattgefunden hat, E-Mail an Autor, mit Link, um Stattfinden zu bestätigen

    @transition(field=state,
                source=['ANGEMELDET', 'ABGELEHNT', 'ABGESAGT'],
                target='ZUGESAGT',
                permission='seminars.can_zusagen',
                custom=dict(button_name="Zusagen", color="primary"))
    def zusagen(self):
        # Email: author, Gruppenhut
        pass

    @transition(field=state,
                source=['ZUGESAGT'],
                target='ABGESAGT',
                permission='seminars.can_absagen',
                custom=dict(button_name="Absagen", color="danger"))
    def absagen(self):
        # Email: author, Gruppenhut, verwalter
        pass

    @transition(field=state,
                source=['ANGEMELDET', 'ZUGESAGT'],
                target='ABGELEHNT',
                permission='seminars.can_ablehnen',
                custom=dict(button_name="Ablehnen", color="danger"))
    def ablehnen(self):
        # Email: author, Gruppenhut
        pass

    @transition(field=state,
                source=['ANGEMELDET', 'ZUGESAGT'],
                target='ZURUECKGEZOGEN',
                permission='seminars.can_zurueckziehen',
                custom=dict(button_name="Zurückziehen", color="danger"))
    def zurueckziehen(self):
        # Email: author, Gruppenhut, verwalter
        pass

    @transition(field=state,
                source=['ZUGESAGT'],
                target='STATTGEFUNDEN',
                permission='seminars.can_stattfinden',
                custom=dict(button_name="Stattfinden bestätigen", color="primary"),
                conditions=[is_in_the_past])
    def stattfinden(self):
        # Email: an Gruppenhut
        pass

    @transition(field=state,
                source=['STATTGEFUNDEN'],
                target='OHNE_ABRECHNUNG',
                permission='seminars.can_ohne_abrechnung',
                custom=dict(button_name="ohne Abrechnung", color="danger"))
    def ohne_abrechnung(self):
        # keine Mail
        pass

    @transition(field=state,
                source=['STATTGEFUNDEN'],
                target='ABGESCHICKT',
                permission='seminars.can_abschicken',
                custom=dict(button_name="Abrechnung abgeschickt", color="primary"))
    def abschicken(self):
        # keine Mail
        pass

    @transition(field=state,
                source=['STATTGEFUNDEN', 'ABGESCHICKT'],
                target='ANGEKOMMEN',
                permission='seminars.can_ankommen',
                custom=dict(button_name="Abrechnung angekommen", color="primary"))
    def ankommen(self):
        # Mail an Autor
        pass

    @transition(field=state,
                source=['ANGEKOMMEN'],
                target='RECHNERISCH',
                permission='seminars.can_rechnen',
                custom=dict(button_name="rechnerische Prüfung", color="primary"))
    def rechnen(self):
        # keine Mail
        pass

    @transition(field=state,
                source=['RECHNERISCH'],
                target='INHALTLICH',
                permission='seminars.can_inhalten',
                custom=dict(button_name="inhaltliche Prüfung", color="primary"))
    def inhalten(self):
        # keine Mail
        pass

    @transition(field=state,
                source=['INHALTLICH'],
                target='NACHPRUEFUNG',
                permission='seminars.can_nach_pruefen',
                custom=dict(button_name="Nachprüfung", color="primary"))
    def nach_pruefen(self):
        # keine Mail
        pass

    @transition(field=state,
                source=['NACHPRUEFUNG'],
                target='FERTIG',
                permission='seminars.can_fertigen',
                custom=dict(button_name="Prüfung abschließen", color="primary"))
    def fertigen(self):
        # Mail an Autor
        pass

    @transition(field=state,
                source=['FERTIG'],
                target='UEBERWIESEN',
                permission='seminars.can_ueberweisen',
                custom=dict(button_name="Überweisung bestätigen", color="primary"))
    def ueberweisen(self):
        # keine Mail
        pass

    @transition(field=state,
                source=['NACHPRUEFUNG', 'INHALTLICH', 'ANGEKOMMEN'],
                target='UNMOEGLICH',
                permission='seminars.can_unmoeglichen',
                custom=dict(button_name="Abrechnung unmöglich", color="danger"))
    def unmoeglichen(self):
        # keine Mail
        pass


@rules.predicate
def is_seminar_author(user, seminar):
    if seminar:
        return seminar.author == user
    return False
@rules.predicate
def has_group_hat_for_seminar(user, seminar):
    if seminar:
        return seminar.group in user.group_hats.all()
    return False
@rules.predicate
def has_janun_group_for_seminar(user, seminar):
    if seminar:
        return seminar.group in user.janun_groups.all()
    return False
@rules.predicate
def just_created(user, seminar):
    if seminar:
        return seminar.created > (timezone.now() - timedelta(minutes=5))
    return False


rules.add_perm('seminars.can_see_all_seminars', is_verwalter)
rules.add_perm('seminars.see_stats', is_verwalter | is_pruefer)
rules.add_perm(
    'seminars.detail_seminar',
    is_verwalter | is_seminar_author | has_group_hat_for_seminar | has_janun_group_for_seminar & is_reviewed)
rules.add_perm('seminars.change_seminar', is_verwalter | is_seminar_author | has_group_hat_for_seminar)
rules.add_perm('seminars.delete_seminar', is_verwalter | is_seminar_author & just_created)

# perms for transitions
rules.add_perm('seminars.can_zusagen',          is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_absagen',          is_verwalter | has_group_hat_for_seminar | is_seminar_author)
rules.add_perm('seminars.can_ablehnen',         is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_zurueckziehen',    is_verwalter | has_group_hat_for_seminar | is_seminar_author)
rules.add_perm('seminars.can_stattfinden',      is_verwalter | has_group_hat_for_seminar | is_seminar_author)
rules.add_perm('seminars.can_ohne_abrechnung',  is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_abschicken',       is_verwalter | has_group_hat_for_seminar | is_seminar_author)
rules.add_perm('seminars.can_ankommen',         is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_rechnen',          is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_inhalten',         is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_nach_pruefen',     is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_fertigen',         is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_ueberweisen',      is_verwalter | has_group_hat_for_seminar)
rules.add_perm('seminars.can_unmoeglichen',     is_verwalter | has_group_hat_for_seminar)

rules.add_perm('seminars.verwendungsnachweis',     is_verwalter)


class SeminarComment(TimeStampedModel, models.Model):
    seminar = models.ForeignKey(
        Seminar,
        related_name="comments",
        verbose_name="Seminar",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        verbose_name="Autor_in",
        on_delete=models.SET_NULL,
        null=True,
    )
    comment = models.TextField("Kommentartext")
    is_internal = models.BooleanField(
        "interner Vermerk", default=False,
        help_text="Sehen nur Prüfer und Verwalter"
    )


@rules.predicate
def is_comment_author(user, comment):
    if comment:
        return comment.author == user
    return False


rules.add_perm('seminars.delete_seminar_comment', is_verwalter | is_comment_author)
rules.add_perm('seminars.see_internal_comment', is_verwalter | is_pruefer | is_comment_author)
rules.add_perm('seminars.create_internal_comment', is_verwalter | is_pruefer)
