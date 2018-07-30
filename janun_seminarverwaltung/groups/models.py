from django.db import models
from django.urls import reverse

import rules
from janun_seminarverwaltung.users.models import is_verwalter


def logo_filename(instance, filename):
    return "groups/{0}/{1}".format(instance.name, filename)


class JANUNGroup(models.Model):
    name = models.CharField("Name", max_length=255, unique=True)
    logo = models.ImageField(
        verbose_name="Logo", blank=True, null=True,
        upload_to=logo_filename
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('groups:detail', args=[self.pk])

    class Meta:
        ordering = ["name"]
        verbose_name = "JANUN-Gruppe"
        verbose_name_plural = "JANUN-Gruppen"
        permissions = (
            ('detail_janungroup', "Kann Gruppendaten sehen"),
            ('can_see_all_janungroups', "Kann alle Gruppen sehen")
        )


@rules.predicate
def is_member(user, group):
    return user in group.members.all()


@rules.predicate
def has_group_hat(user, group):
    return user in group.group_hats.all()


rules.add_perm('groups.can_see_all_janungroups', is_verwalter)
rules.add_perm('groups.detail_janungroup', is_verwalter | is_member | has_group_hat)
rules.add_perm('groups.add_janungroup', is_verwalter)
rules.add_perm('groups.change_janungroup', is_verwalter | is_member | has_group_hat)
rules.add_perm('groups.delete_janungroup', is_verwalter)
