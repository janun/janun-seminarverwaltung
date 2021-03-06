# Generated by Django 2.2.11 on 2020-03-27 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emails', '0008_auto_20200311_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailattachment',
            name='filename',
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='cc_template',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='CC'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='from_template',
            field=models.CharField(default='seminare@janun.de', max_length=255, verbose_name='Von'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='template_key',
            field=models.CharField(choices=[('seminar_applied', 'Seminar angemeldet'), ('seminar_delete', 'Seminar gelöscht'), ('seminar_update', 'Seminar geändert'), ('seminar_deadline_expired', 'Seminar Abrechnungsfrist abgelaufen'), ('seminar_deadline_soon', 'Seminar Abrechnungsfrist in 14 Tagen'), ('seminar_occurred', 'Seminar stattgefunden (Enddatum Vergangenheit)'), ('user_signup', 'Benutzer registriert')], max_length=255, verbose_name='Grundbedingung'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='to_template',
            field=models.CharField(default='{{ seminar.owner.email }}', max_length=255, verbose_name='An'),
        ),
        migrations.AlterField(
            model_name='emailtemplatecondition',
            name='expression',
            field=models.CharField(help_text="z.B. user.role == 'Teamer_in'", max_length=255, verbose_name='Nebenbedingung'),
        ),
        migrations.CreateModel(
            name='HistoricalEmailTemplate',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Aktiv')),
                ('template_key', models.CharField(choices=[('seminar_applied', 'Seminar angemeldet'), ('seminar_delete', 'Seminar gelöscht'), ('seminar_update', 'Seminar geändert'), ('seminar_deadline_expired', 'Seminar Abrechnungsfrist abgelaufen'), ('seminar_deadline_soon', 'Seminar Abrechnungsfrist in 14 Tagen'), ('seminar_occurred', 'Seminar stattgefunden (Enddatum Vergangenheit)'), ('user_signup', 'Benutzer registriert')], max_length=255, verbose_name='Grundbedingung')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Beschreibung')),
                ('from_template', models.CharField(default='seminare@janun.de', max_length=255, verbose_name='Von')),
                ('to_template', models.CharField(default='{{ seminar.owner.email }}', max_length=255, verbose_name='An')),
                ('cc_template', models.CharField(blank=True, max_length=255, null=True, verbose_name='CC')),
                ('text_template', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('subject_template', models.CharField(blank=True, max_length=255, null=True, verbose_name='Betreff')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical E-Mail-Vorlage',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
