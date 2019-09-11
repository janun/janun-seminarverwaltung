# Generated by Django 2.2.4 on 2019-09-09 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0007_auto_20190909_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='advance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Vorschuss'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seminars', to=settings.AUTH_USER_MODEL, verbose_name='Eigentümer_in'),
        ),
    ]