# Generated by Django 2.2.11 on 2020-03-11 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0005_auto_20200306_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplatecondition',
            name='expression',
            field=models.CharField(max_length=255, verbose_name='Bedingung'),
        ),
    ]