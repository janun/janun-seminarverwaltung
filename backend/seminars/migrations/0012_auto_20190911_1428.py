# Generated by Django 2.2.5 on 2019-09-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0011_seminar_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='deadline',
            field=models.DateField(verbose_name='Abrechnungsdeadline'),
        ),
    ]
