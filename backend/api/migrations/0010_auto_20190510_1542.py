# Generated by Django 2.2.1 on 2019-05-10 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_seminar_last_visit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seminar',
            name='last_visit',
        ),
        migrations.AddField(
            model_name='user',
            name='last_visit',
            field=models.DateTimeField(null=True),
        ),
    ]