# Generated by Django 2.2.5 on 2019-09-14 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0016_auto_20190914_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seminar',
            name='deadline',
        ),
    ]