# Generated by Django 2.2.7 on 2019-11-05 19:19

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20191024_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=255, verbose_name='Voller Name')),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'invalid': 'Bitte gültige Telefonnummer eingeben, z.B. 0511 1241512'}, max_length=128, region=None, verbose_name='Telefonnummer')),
                ('role', models.CharField(choices=[('Teamer_in', 'Teamer_in'), ('Prüfer_in', 'Prüfer_in'), ('Verwalter_in', 'Verwalter_in')], default='Teamer_in', max_length=255, verbose_name='Rolle')),
                ('is_reviewed', models.BooleanField(default=False, verbose_name='überprüft')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Erstellt am')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Geändert am')),
                ('last_visit', models.DateTimeField(null=True, verbose_name='Letzter Besuch')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Konto',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalJANUNSeminarPreferences',
            fields=[
                ('preferences_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='preferences.Preferences')),
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('help_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Hilfe-Telefon')),
                ('help_email', models.EmailField(blank=True, max_length=254, verbose_name='Hilfe-E-Mail')),
                ('seminar_policy_url', models.URLField(blank=True, verbose_name='Link Seminarrichtlinie')),
                ('data_protection_policy_url', models.URLField(blank=True, verbose_name='Link Datenschutzrichtlinie')),
                ('legal_url', models.URLField(default='https://www.janun.de/impressum', verbose_name='Link zum Impressum')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Einstellung',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
