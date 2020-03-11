# Generated by Django 2.2.10 on 2020-03-06 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0004_auto_20200305_2153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailattachment',
            options={'verbose_name': 'E-Mail-Anhang', 'verbose_name_plural': 'E-Mail-Anhänge'},
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='template_key',
            field=models.CharField(choices=[('seminar_applied', 'Seminar angemeldet'), ('seminar_delete', 'Seminar gelöscht'), ('seminar_update', 'Seminar geändert'), ('user_signup', 'Benutzer registriert')], help_text='Wann diese E-Mail verschickt werden soll', max_length=255, verbose_name='Grundbedingung'),
        ),
        migrations.CreateModel(
            name='EmailTemplateCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.CharField(help_text='z.B. <code>seminar.owner == user</code>', max_length=255, verbose_name='Weitere Bedingung')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='emails.EmailTemplate')),
            ],
        ),
    ]