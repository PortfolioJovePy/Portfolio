from django.db import models
from django.core.validators import FileExtensionValidator

class Contatos(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    nascimento = models.CharField(verbose_name='Data de Nascimento')
    contatos_estabelecidos = models.IntegerField(verbose_name='Contatos estabelecidos')    
    negocios_realizados = models.IntegerField(verbose_name='Negócios realizados')   
    faturamento = models.IntegerField(verbose_name='Valor faturado')   
    lucro = models.IntegerField(verbose_name='Valor do lucro')   
    
    def __str__(self):
        return self.email

class UploadTemplate(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    arquivo = models.FileField(
        upload_to='uploads_html/', 
        validators=[FileExtensionValidator(allowed_extensions=['html'])],
        verbose_name="Arquivo HTML"
    )
    data_upload = models.DateTimeField(auto_now_add=True, verbose_name="Data do Upload")

    def __str__(self):
        return self.nome
    
class AgendarEmail(models.Model):
    email = models.ForeignKey(Contatos, on_delete=models.CASCADE, verbose_name="E-mail")
    assunto = models.CharField(max_length=255, verbose_name="Assunto")    
    send_date = models.DateField(verbose_name="Data de Envio")
    send_time = models.TimeField(verbose_name="Hora de Envio")
    email_template = models.ForeignKey(UploadTemplate, on_delete=models.CASCADE, verbose_name="Template do E-mail")
    enviado = models.BooleanField(default=False, verbose_name="Mensagem Enviada")
    periodo = models.CharField(max_length=255, choices=[('nao repete','não repete'),
                                                        ('diario','diário'),
                                                        ('semanal','semanal'),
                                                        ('mensal','mensal'),
                                                        ('enesimo dia util','enésimo dia útil')],verbose_name='Período')
    
    repeticao = models.CharField(max_length=255, choices=[('Nao repete','Não repete')]+[(str(i),str(i)) for i in list(range(1,32,1))],verbose_name='A cada')
    conteudo_personalizado = models.JSONField(verbose_name='Conteúdo personalizado')
    def __str__(self):
        status = "Enviada" if self.enviado else "Não Enviada"
        return f"Mensagem para {self.email} em {self.send_date} às {self.send_time} - {status}"
