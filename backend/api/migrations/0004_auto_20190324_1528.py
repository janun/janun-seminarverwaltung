# Generated by Django 2.1.7 on 2019-03-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190321_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminar',
            name='status',
            field=models.CharField(choices=[('angemeldet', 'angemeldet'), ('zurückgezogen', 'zurückgezogen'), ('zugesagt', 'zugesagt'), ('abgelehnt', 'abgelehnt'), ('abgesagt', 'abgesagt'), ('stattgefunden', 'stattgefunden'), ('ohne Abrechnung', 'ohne Abrechnung'), ('Abrechnung abgeschickt', 'Abrechnung abgeschickt'), ('Abrechnung angekommen', 'Abrechnung angekommen'), ('Abrechnung unmöglich', 'Abrechnung unmöglich'), ('rechnerische Prüfung', 'rechnerische Prüfung'), ('inhaltliche Prüfung', 'inhaltliche Prüfung'), ('Nachprüfung', 'Nachprüfung'), ('fertig geprüft', 'fertig geprüft'), ('überwiesen', 'überwiesen')], default='angemeldet', max_length=255),
        ),
    ]
