from django.urls import path
from .views import *


urlpatterns = [
    path("painel-geral/", gerenciador.as_view(template='painel.html'),name='painel_email'),
    path("contatos/", gerenciador.as_view(template='contatos.html'),name='contatos'),
    path("agendamento/", gerenciador.as_view(template='agendamento.html'),name='agendamento'),
    path("upload-template/", gerenciador.as_view(template='upload_template.html'),name='upload_template'),
    path('crm/',crm_view, name='crm'),
    path('salvar_contato/', salvar_contato, name='salvar_contato'),


]

