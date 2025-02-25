from django.db import models

class ContatoDuvidaEmail(models.Model): #email de contato
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
    