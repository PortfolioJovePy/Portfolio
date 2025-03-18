from django.urls import path
from .views import *


urlpatterns = [
    
    path("", gerenciador.as_view(template='painel.html'),name='painel_email'),
    path('crm/',gerenciador.as_view(template='CRM.html'), name='crm'),
    path("contatos/", gerenciador.as_view(template='contatos.html'),name='contatos'),
    path("agendamento/", gerenciador.as_view(template='agendamento.html'),name='agendamento'),
    path("upload-template/", gerenciador.as_view(template='upload_template.html'),name='upload_template'),
    

    
    path("criar-template/", gerenciador.as_view(template='criador_template_emails.html'),name='criar_template'),
    path("ver-templates/", gerenciador.as_view(template='templates_email.html'),name='listar_templates'),
    #acoes
    path('deletar/<int:template_id>/', deletar_template, name='deletar_template'),
    path('ver-templates/<int:template_id>/', visualizar_template, name='visualizar_template'),
    path('editar/<int:template_id>/', editar_template, name='editar_template'),
    
    path('salvar_contato/', salvar_contato, name='salvar_contato'),
    path('deletar_contato/', deletar_contato, name='deletar_contato'),    

    path("salvar_template/", salvar_template, name="salvar_template"),



]

