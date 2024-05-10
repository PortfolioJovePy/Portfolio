from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    respondido = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.nome} ({self.email})"


class Newsletter(models.Model):    
    email = models.EmailField(unique=True)    
    def __str__(self):
        return self.email
    
class Visitantes(models.Model):    
    ip = models.EmailField(unique=True)
    data = models.DateField(auto_created=True)
    entrada = models.DateTimeField(auto_now_add=True)
    saida = models.DateTimeField(blank=True, null=True)
    tempo_sessao = models.DurationField(blank=True, null=True)
    pais = models.CharField(max_length=200)
    regiao = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)