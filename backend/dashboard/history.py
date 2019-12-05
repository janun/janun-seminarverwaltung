from operator import attrgetter
import json
import itertools
import datetime

from django.db import models

from simple_history.models import registered_models


def json_converter(value):
    if isinstance(value, datetime.date):
        return value.strftime("%d.%m.%Y")
    return str(value)


class BaseHistoricalModel(models.Model):
    """Base class for Historical Models
    that saves changes as json in history_change_reason
    """

    def get_history_changes(self) -> str:
        if self.history_type == "~":  # pylint: disable=no-member
            prev_record = self.prev_record  # pylint: disable=no-member
            if prev_record:
                changes = self.diff_against(  # pylint: disable=no-member
                    prev_record
                ).changes
                if changes:
                    return json.dumps(
                        list(map(lambda c: c.__dict__, changes)), default=json_converter
                    )

    def save(self, *args, **kwargs):
        self.history_change_reason = self.get_history_changes()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


def get_global_history(limit=10, offset=0):
    history = []
    for model in registered_models.values():
        for entry in model.history.all().select_related("history_user")[
            offset : limit + offset
        ]:
            history.append(entry)
    history = sorted(history, key=attrgetter("history_date"), reverse=True)
    # filter out empty changes:
    history = filter(
        lambda e: e.history_type != "~" or e.history_change_reason, history
    )
    return itertools.islice(history, limit)
