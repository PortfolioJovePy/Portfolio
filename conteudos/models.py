from django.db import models

# Create your models here.
class Conteudo(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=500)
    titulo_ingles = models.CharField(max_length=100)
    descricao_ingles = models.CharField(max_length=500)
    link = models.CharField(max_length=10000)
    link_imagem = models.CharField(max_length=10000)
    link_notbook = models.CharField(max_length=10000)


class LancamentoEbook1(models.Model):    
    email = models.EmailField(unique=True)    
    lancamento = models.DateField(auto_now_add=True)    
    def __str__(self):
        return self.email
    
class Leituras(models.Model):
    titulo = models.CharField(max_length=100)
    resumo = models.CharField(max_length=500)
    titulo_ingles = models.CharField(max_length=100)
    resumo_ingles = models.CharField(max_length=500)
    link = models.CharField(max_length=10000)


class Ebooks(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=500)
    titulo_ingles = models.CharField(max_length=100)
    descricao_ingles = models.CharField(max_length=500)
    link_imagem = models.CharField(max_length=10000)
    valor = models.CharField(max_length=500)
    