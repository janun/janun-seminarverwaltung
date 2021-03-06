# Generated by Django 2.2.6 on 2019-10-22 08:43

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_janunseminarpreferences'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='janunseminarpreferences',
            options={'verbose_name': 'Einstellung', 'verbose_name_plural': 'Einstellungen'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AlterField(
            model_name='janunseminarpreferences',
            name='data_protection_policy_url',
            field=models.URLField(blank=True, verbose_name='Link Datenschutzrichtlinie'),
        ),
        migrations.AlterField(
            model_name='janunseminarpreferences',
            name='help_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Hilfe-E-Mail'),
        ),
        migrations.AlterField(
            model_name='janunseminarpreferences',
            name='help_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Hilfe-Telefon'),
        ),
        migrations.AlterField(
            model_name='janunseminarpreferences',
            name='seminar_policy_url',
            field=models.URLField(blank=True, verbose_name='Link Seminarrichtlinie'),
        ),
    ]
