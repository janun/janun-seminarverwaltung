# Generated by Django 2.2.10 on 2020-03-04 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_key', models.CharField(help_text='zur internen Benutzung', max_length=255, unique=True, verbose_name='Kurzname')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Beschreibung')),
                ('text_template', models.TextField(blank=True, null=True, verbose_name='Vorlage für den Text der E-Mail')),
                ('subject_template', models.CharField(blank=True, max_length=255, null=True, verbose_name='Vorlage für den Betreff der E-Mail')),
            ],
            options={
                'verbose_name': 'E-Mail-Vorlage',
                'verbose_name_plural': 'E-Mail-Vorlagen',
            },
        ),
        migrations.CreateModel(
            name='EmailAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='email_attachments/', verbose_name='Datei')),
                ('filename', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dateiname')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='emails.EmailTemplate')),
            ],
        ),
    ]