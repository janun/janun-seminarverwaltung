# Generated by Django 2.2.5 on 2019-09-11 12:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0010_auto_20190909_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminar',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 11, 12, 23, 49, 34019, tzinfo=utc), verbose_name='Abrechnungsdeadline'),
            preserve_default=False,
        ),
    ]
