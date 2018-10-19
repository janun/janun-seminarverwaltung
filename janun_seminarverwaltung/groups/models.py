from django.db import models
from django.urls import reverse

import rules
from phonenumber_field.modelfields import PhoneNumberField

from janun_seminarverwaltung.users.models import is_verwalter, is_reviewed


def logo_filename(instance, filename):
    return "groups/{0}/{1}".format(instance.name, filename)


class JANUNGroup(models.Model):
    name = models.CharField("Name", max_length=255, unique=True)
    logo = models.ImageField(
        verbose_name="Logo", blank=True, null=True,
        upload_to=logo_filename
    )
    homepage = models.URLField("Homepage", blank=True, null=True)
    email = models.EmailField("E-Mail-Adresse", blank=True, null=True)
    address = models.TextField("Postadresse", blank=True, null=True)

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


class ContactPerson(models.Model):
    name = models.CharField("Name", max_length=255)
    email = models.EmailField("E-Mail", blank=True, null=True)
    phone = PhoneNumberField("Telefonnummer", blank=True)
    group = models.ForeignKey(JANUNGroup, on_delete=models.CASCADE, related_name='contact_people')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


@rules.predicate
def is_member(user, group):
    return user in group.members.all()


@rules.predicate
def has_group_hat(user, group):
    return user in group.group_hats.all()


rules.add_perm('groups.can_see_all_janungroups', is_verwalter)
rules.add_perm('groups.detail_janungroup', is_verwalter | is_member & is_reviewed | has_group_hat)
rules.add_perm('groups.add_janungroup', is_verwalter)
rules.add_perm('groups.change_janungroup', is_verwalter | is_member & is_reviewed | has_group_hat)
rules.add_perm('groups.delete_janungroup', is_verwalter)
