# Generated by Django 2.1.1 on 2018-09-12 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20180912_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='janungroup',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Postadresse'),
        ),
    ]
