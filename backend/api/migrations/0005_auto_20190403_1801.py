# Generated by Django 2.1.7 on 2019-04-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190324_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminar',
            name='description',
            field=models.TextField(default='keine Beschreibung eingetragen'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='planned_attendees_max',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='planned_attendees_min',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='planned_training_days',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='requested_funding',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]