# Generated by Django 5.0 on 2024-05-06 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conteudos', '0003_conteudo_descricao_ingles_conteudo_titulo_ingles'),
    ]

    operations = [
        migrations.CreateModel(
            name='LancamentoEbook1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]