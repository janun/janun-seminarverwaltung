import datetime
from decimal import Decimal

from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save, post_delete

from model_utils import Choices


def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set('api_updated_at_timestamp', datetime.datetime.utcnow())


class JANUNGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class User(AbstractUser):
    ROLES = Choices("Teamer_in", "Prüfer_in", "Verwalter_in")
    first_name = None
    last_name = None
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=255, choices=ROLES,
                            default=ROLES['Teamer_in'])
    telephone = models.CharField(max_length=100, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    janun_groups = models.ManyToManyField(
        JANUNGroup, related_name='members', blank=True)
    group_hats = models.ManyToManyField(
        JANUNGroup, related_name='group_hats', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('name',)


class Seminar(models.Model):
    # manual data migrations needed if changed!
    STATES = Choices(
        'angemeldet',
        'zurückgezogen',
        'zugesagt',
        'abgelehnt',
        'abgesagt',
        'stattgefunden',
        'ohne Abrechnung',
        'Abrechnung abgeschickt',
        'Abrechnung angekommen',
        'Abrechnung unmöglich',
        'rechnerische Prüfung',
        'inhaltliche Prüfung',
        'Nachprüfung',
        'fertig geprüft',
        'überwiesen',
    )
    # NORMAL_STATES = Choices(
    #     'angemeldet',
    #     'zugesagt',
    #     'abgesagt',
    #     'stattgefunden',
    #     'Abrechnung abgeschickt',
    #     'Abrechnung angekommen',
    #     'rechnerische Prüfung',
    #     'inhaltliche Prüfung',
    #     'Nachprüfung',
    #     'fertig geprüft',
    #     'überwiesen',
    # )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=STATES, default=STATES.angemeldet)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='seminars')
    group = models.ForeignKey(
        JANUNGroup, on_delete=models.SET_NULL, null=True, related_name='seminars')

    description = models.TextField(blank=True, null=True)

    start_date = models.DateField(db_index=True)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField()
    end_time = models.TimeField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True, null=True)

    planned_training_days = models.PositiveSmallIntegerField()
    planned_attendees_min = models.PositiveSmallIntegerField()
    planned_attendees_max = models.PositiveSmallIntegerField()
    requested_funding = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tnt(self):
        return self.planned_attendees_max * self.planned_training_days

    @property
    def tnt_cost(self):
        if self.tnt == 0:
            return 0
        return round(Decimal(self.requested_funding / self.tnt), 2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-start_date',)


for model in [Seminar, ]:
    post_save.connect(receiver=change_api_updated_at, sender=model)
    post_delete.connect(receiver=change_api_updated_at, sender=model)


class SeminarComment(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='comments')
    seminar = models.ForeignKey(
        Seminar, on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_at',)
