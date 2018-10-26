from django.db import models
from django.db.models import F


class SeminarStats(object):
    def __init__(self, qs):
        self.qs = qs

    @property
    def count(self):
        return self.qs.count()

    @property
    def requested_funding(self):
        return self.qs.aggregate(funding=models.Sum('requested_funding'))['funding']

    @property
    def requested_tnt(self):
        return self.qs.aggregate(tnt=models.Sum(
            F('planned_training_days') * F('planned_attendees_max'),
            output_field=models.IntegerField()
        ))['tnt']

    @property
    def requested_funding_over_tnt(self):
        if self.requested_tnt:
            return self.requested_funding / self.requested_tnt
        return 0.0
