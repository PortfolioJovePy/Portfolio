# Generated by Django 5.1.6 on 2025-02-25 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0008_visitantes_cidade_visitantes_pais_visitantes_regiao'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contato',
            new_name='ContatoDuvidaEmail',
        ),
        migrations.DeleteModel(
            name='Visitantes',
        ),
    ]
