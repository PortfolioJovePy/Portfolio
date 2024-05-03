from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()

    def __str__(self):
        return f"{self.nome} ({self.email})"


class Newsletter(models.Model):    
    email = models.EmailField(unique=True)    
    def __str__(self):
        return self.email