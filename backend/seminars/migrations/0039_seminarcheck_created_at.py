# Generated by Django 2.2.11 on 2020-03-11 14:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0038_seminarcheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminarcheck',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
