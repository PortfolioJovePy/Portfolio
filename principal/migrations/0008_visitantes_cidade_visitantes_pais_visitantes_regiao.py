# Generated by Django 5.0 on 2024-05-10 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0007_visitantes'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitantes',
            name='cidade',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visitantes',
            name='pais',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visitantes',
            name='regiao',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]