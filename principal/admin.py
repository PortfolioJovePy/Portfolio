from django.contrib import admin
from .models import Contato

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')  # Campos a serem exibidos na listagem
    list_filter = ('email',)  # Filtros disponíveis
    search_fields = ('nome', 'email', 'mensagem')  # Campos de pesquisa

admin.site.register(Contato, ContatoAdmin)
