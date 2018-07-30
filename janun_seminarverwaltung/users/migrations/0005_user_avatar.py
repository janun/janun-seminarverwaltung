# Generated by Django 2.0.4 on 2018-07-09 13:14

from django.db import migrations, models
import janun_seminarverwaltung.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180709_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=janun_seminarverwaltung.users.models.avatar_filename, verbose_name='Profilbild'),
        ),
    ]
