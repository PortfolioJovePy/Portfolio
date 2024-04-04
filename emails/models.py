from django.db import models

class Contatos(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    nascimento = models.DateField(verbose_name='Data de Nas cimento')
    contatos_estabelecidos = models.IntegerField(verbose_name='Contatos estabelecidos')    
    negocios_realizados = models.IntegerField(verbose_name='Negócios realizados')    

class AgendarEmail(models.Model):
    nome = models.ForeignKey(Contatos, on_delete=models.CASCADE, verbose_name="Nome")
    send_date = models.DateField(verbose_name="Data de Envio")
    send_time = models.TimeField(verbose_name="Hora de Envio")
    email_template = models.TextField(verbose_name="Template do E-mail")
    enviado = models.BooleanField(default=False, verbose_name="Mensagem Enviada")
    
    def __str__(self):
        status = "Enviada" if self.is_sent else "Não Enviada"
        return f"Mensagem para {self.conato.nome} em {self.send_date} às {self.send_time} - {status}"