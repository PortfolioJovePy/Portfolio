from django.contrib import admin
from .models import Conteudo

class ConteudoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'link', 'link_imagem', 'link_notbook')  # Campos a serem exibidos na lista
    search_fields = ('titulo', 'descricao')  # Campos pesquisáveis

# Registrar o modelo com personalização
admin.site.register(Conteudo, ConteudoAdmin)
