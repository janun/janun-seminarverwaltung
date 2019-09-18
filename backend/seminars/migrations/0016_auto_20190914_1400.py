# Generated by Django 2.2.5 on 2019-09-14 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0015_auto_20190913_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seminars', to=settings.AUTH_USER_MODEL, verbose_name='Eigentümer_in'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='planned_attendees_max',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='geplante TN max.'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='planned_attendees_min',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='geplante TN min.'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='planned_training_days',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='geplante Bildungstage'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='requested_funding',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='angeforderte Förderung'),
        ),
    ]