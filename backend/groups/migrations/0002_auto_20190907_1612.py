# Generated by Django 2.2.4 on 2019-09-07 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='janungroup',
            options={'ordering': ('name',), 'verbose_name': 'JANUN-Gruppe', 'verbose_name_plural': 'JANUN-Gruppen'},
        ),
        migrations.AlterField(
            model_name='janungroup',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
    ]
