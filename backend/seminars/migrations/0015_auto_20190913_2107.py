# Generated by Django 2.2.5 on 2019-09-13 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0014_auto_20190913_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='planned_attendees_max',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='geplante TN max.'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='planned_attendees_min',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='geplante TN min.'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='planned_training_days',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='geplante Bildungstage'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='requested_funding',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='angeforderte Förderung'),
        ),
    ]