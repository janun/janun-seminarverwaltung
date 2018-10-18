# Generated by Django 2.1.1 on 2018-10-15 12:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0011_auto_20181015_1344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seminar',
            options={'ordering': ['start_date', 'start_time'], 'permissions': (('detail_seminars', 'Kann Seminardaten sehen'), ('can_see_all_seminars', 'Kann alle Seminare sehen')), 'verbose_name': 'Seminar', 'verbose_name_plural': 'Seminare'},
        ),
        migrations.AddField(
            model_name='seminar',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Enddatum'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='end_time',
            field=models.TimeField(blank=True, default=django.utils.timezone.now, verbose_name='Endzeit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Anfangsdatum'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seminar',
            name='start_time',
            field=models.TimeField(blank=True, default=django.utils.timezone.now, verbose_name='Anfangszeit'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seminar',
            name='title',
            field=models.CharField(help_text='Beschreib oder bennene Dein Seminar in wenigen Worten', max_length=255, unique_for_date='start_date', verbose_name='Titel'),
        )
    ]
