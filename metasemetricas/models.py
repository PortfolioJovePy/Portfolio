from django.db import models


class metas(models.Model):    
    nome = models.CharField(max_length=140)    
    def __str__(self):
        return self.nome
    
class objetivos(models.Model):
    nome_meta = models.ForeignKey(metas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=140)    
    def __str__(self):
        return self.nome


class avaliacao(models.Model):
    objetivo = models.ForeignKey(objetivos, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 101)], help_text="Nota de 1 a 100")
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.objetivo} - Nota: {self.nota}"
