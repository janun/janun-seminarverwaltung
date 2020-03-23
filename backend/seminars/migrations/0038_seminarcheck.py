# Generated by Django 2.2.11 on 2020-03-11 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0037_auto_20200311_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeminarCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_type', models.CharField(blank=True, max_length=255, null=True)),
                ('seminar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='seminars.Seminar')),
            ],
        ),
    ]