# Generated by Django 2.2.5 on 2019-09-29 13:31

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20190907_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='janungroup',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, null=True, populate_from='title', unique=True, verbose_name='URL-Titel'),
        ),
    ]
