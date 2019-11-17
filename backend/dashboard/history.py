from operator import attrgetter
import json

from django.db import models

from simple_history.models import registered_models


class BaseHistoricalModel(models.Model):
    """Base class for Historical Models
    that saves changes as json in history_change_reason
    """

    def get_history_changes(self) -> str:
        if self.history_type == "~":
            prev_record = self.prev_record
            if prev_record:
                changes = self.diff_against(prev_record).changes
                if changes:
                    return json.dumps(list(map(lambda c: c.__dict__, changes)))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_from_db()  # or else dates are strs and cant be serialized
        self.history_change_reason = self.get_history_changes()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# TODO: get a queryset instead of a list
def get_global_history(length=10):
    history = []
    for model in registered_models.values():
        for entry in model.history.all().select_related("history_user")[:length]:
            history.append(entry)
    return sorted(history, key=attrgetter("history_date"), reverse=True)
