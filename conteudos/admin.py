from django.contrib import admin
from .models import *

class ConteudoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'link', 'link_imagem', 'link_notbook')  # Campos a serem exibidos na lista
    search_fields = ('titulo', 'descricao')  # Campos pesquisáveis

class LeiturasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'resumo', 'link')  # Campos a serem exibidos na lista
    search_fields = ('titulo', 'resumo')  # Campos pesquisáveis

class LancamentoEbook1Admin(admin.ModelAdmin):
    list_display = ('email',)  # Campos a serem exibidos na lista
    search_fields = ('email',)  # Campos pesquisáveis


class EbooksAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'valor')  # Campos a serem exibidos na lista
    search_fields = ('titulo', 'descricao')  # Campos pesquisáveis


# Registrar o modelo com personalização
admin.site.register(Conteudo, ConteudoAdmin)
admin.site.register(Leituras, LeiturasAdmin)
admin.site.register(LancamentoEbook1, LancamentoEbook1Admin)
admin.site.register(Ebooks, EbooksAdmin)
