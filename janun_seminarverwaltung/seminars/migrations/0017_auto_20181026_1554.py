# Generated by Django 2.1.1 on 2018-10-26 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0016_auto_20181019_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminar',
            name='planned_attendees_max',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Teilnehmende max.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='planned_attendees_min',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Teilnehmende min.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seminar',
            name='planned_training_days',
            field=models.PositiveSmallIntegerField(verbose_name='Bildungstage'),
        ),
    ]