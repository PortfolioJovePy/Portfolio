from django.contrib import admin
from .models import *

@admin.register(Contatos)
class ContatosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'nascimento', 'contatos_estabelecidos', 'negocios_realizados','faturamento','lucro')
    search_fields = ('nome', 'email')

@admin.register(UploadTemplate)
class UploadTemplateAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_upload')
    search_fields = ('nome',)


@admin.register(HtmlTemplate)
class HtmlTemplateAdmin(admin.ModelAdmin):
    list_display = ('nome', 'template')
    search_fields = ('nome',)


@admin.register(AgendarEmail)
class AgendarEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'assunto','send_date', 'send_time', 'email_template', 'enviado')
    list_filter = ('enviado', 'send_date')
    search_fields = ( 'email__email',)
