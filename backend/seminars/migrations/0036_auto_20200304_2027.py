# Generated by Django 2.2.10 on 2020-03-04 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0035_seminarview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundingrate',
            name='group_limit_formula',
            field=models.CharField(blank=True, help_text='engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450) mit B = Anzahl der Bildungstage', max_length=255, verbose_name='Formel für Gruppen-Limit'),
        ),
        migrations.AlterField(
            model_name='fundingrate',
            name='single_limit_formula',
            field=models.CharField(blank=True, help_text='engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450) mit B = Anzahl der Bildungstage', max_length=255, verbose_name='Formel für Einzelpersonen-Limit'),
        ),
        migrations.AlterField(
            model_name='historicalfundingrate',
            name='group_limit_formula',
            field=models.CharField(blank=True, help_text='engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450) mit B = Anzahl der Bildungstage', max_length=255, verbose_name='Formel für Gruppen-Limit'),
        ),
        migrations.AlterField(
            model_name='historicalfundingrate',
            name='single_limit_formula',
            field=models.CharField(blank=True, help_text='engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450) mit B = Anzahl der Bildungstage', max_length=255, verbose_name='Formel für Einzelpersonen-Limit'),
        ),
        migrations.AlterField(
            model_name='historicalseminar',
            name='confirmed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Zugesagt am'),
        ),
        migrations.AlterField(
            model_name='seminar',
            name='confirmed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Zugesagt am'),
        ),
        migrations.AlterField(
            model_name='seminarview',
            name='seminar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='views', to='seminars.Seminar'),
        ),
    ]
