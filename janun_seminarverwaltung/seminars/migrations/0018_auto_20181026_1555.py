# Generated by Django 2.1.1 on 2018-10-26 13:55

from django.db import migrations


def add_planned_attendees(apps, schema_editor):
    Seminar = apps.get_model('seminars', 'Seminar')
    for seminar in Seminar.objects.all().iterator():
        if seminar.planned_attendees:
            seminar.planned_attendees_min = seminar.planned_attendees.lower
            seminar.planned_attendees_max = seminar.planned_attendees.upper
        seminar.save()


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0017_auto_20181026_1554'),
    ]

    operations = [
        migrations.RunPython(add_planned_attendees)
    ]
