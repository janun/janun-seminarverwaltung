# Generated by Django 2.2.6 on 2019-10-23 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20191022_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='janunseminarpreferences',
            name='legal_url',
            field=models.URLField(default='https://www.janun.de/impressum', verbose_name='Link zum Impressum'),
        ),
    ]
