# Generated by Django 2.2.5 on 2019-09-09 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0009_auto_20190909_1159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seminar',
            old_name='attendees_jfg',
            new_name='actual_attendees_jfg',
        ),
        migrations.RenameField(
            model_name='seminar',
            old_name='attendees_total',
            new_name='actual_attendees_total',
        ),
        migrations.RenameField(
            model_name='seminar',
            old_name='attendence_days_jfg',
            new_name='actual_attendence_days_jfg',
        ),
        migrations.RenameField(
            model_name='seminar',
            old_name='attendence_days_total',
            new_name='actual_attendence_days_total',
        ),
    ]
