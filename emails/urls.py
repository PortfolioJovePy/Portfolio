from django.urls import path
from .views import *

urlpatterns = [
    path("contatos/", gerenciador.as_view(template='contatos.html'),name='contatos'),
    path("agendamento/", gerenciador.as_view(template='agendamento.html'),name='agendamento'),
    path("upload-template/", gerenciador.as_view(template='upload_template.html'),name='upload_template'),
    path("teste/", email_teste,name='email-teste'),
]

