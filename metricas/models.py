from django.db import models
# Create your models here.
class Metasdelongoprazo(models.Model):    
    nome = models.CharField(max_length=140)  
    status = models.CharField(
        max_length=20,
        choices=[('<20%', '<20%'), ('>=20%', '>=20%'), ('Concluído', 'Concluído')],
        default='<=20%'
    )
    def __str__(self):
        return self.nome
  
    
    
class Objetivosmarco(models.Model):
    nome_meta = models.ForeignKey(Metasdelongoprazo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=140)   
    status = models.CharField(
        max_length=20,
        choices=[('Em Progresso', 'Em Progresso'), ('Concluído', 'Concluído')],
        default='Em Progresso'
    ) 
    def __str__(self):
        return self.nome

class Microobjetivos(models.Model):
    nome_objetivomarco = models.ForeignKey(Objetivosmarco, on_delete=models.CASCADE)
    nome = models.CharField(max_length=140)    
    def __str__(self):
        return self.nome

class Computarevolucao(models.Model):
    objetivo = models.ForeignKey(Microobjetivos, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 101)], help_text="Nota de 1 a 100")
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.objetivo} - Nota: {self.nota}"
