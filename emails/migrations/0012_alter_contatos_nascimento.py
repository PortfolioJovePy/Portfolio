# Generated by Django 5.1.6 on 2025-03-06 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0011_remove_agendaremail_conteudo_personaliado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contatos',
            name='nascimento',
            field=models.CharField(verbose_name='Data de Nascimento'),
        ),
    ]
