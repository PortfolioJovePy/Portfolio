# Generated by Django 5.0 on 2024-05-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_delete_visitantes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_created=True)),
                ('ip', models.EmailField(max_length=254, unique=True)),
                ('entrada', models.DateTimeField(auto_now_add=True)),
                ('saida', models.DateTimeField(blank=True, null=True)),
                ('tempo_sessao', models.DurationField(blank=True, null=True)),
            ],
        ),
    ]
