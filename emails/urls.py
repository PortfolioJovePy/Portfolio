from django.urls import path
from .views import *


urlpatterns = [
    path("painel-geral/", gerenciador.as_view(template='painel.html'),name='painel_email'),
    path("contatos/", gerenciador.as_view(template='contatos.html'),name='contatos'),
    path("agendamento/", gerenciador.as_view(template='agendamento.html'),name='agendamento'),
    path("upload-template/", gerenciador.as_view(template='upload_template.html'),name='upload_template'),
    path("criar-template/", gerenciador.as_view(template='criador_template_emails.html'),name='criar_template'),
    path('salvar-elemento/', salvar_elemento, name='salvar_elemento'),
    path('crm/',gerenciador.as_view(template='CRM.html'), name='crm'),
    path('salvar_contato/', salvar_contato, name='salvar_contato'),
    path('deletar_contato/', deletar_contato, name='deletar_contato'),



]

