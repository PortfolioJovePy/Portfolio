from django.db import models

# Create your models here.
class Conteudo(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=500)
    link = models.CharField(max_length=10000)
    link_imagem = models.CharField(max_length=10000)
    