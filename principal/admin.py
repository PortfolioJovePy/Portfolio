from django.contrib import admin
from .models import *

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email','respondido')  # Campos a serem exibidos na listagem
    list_filter = ('email','email','respondido')  # Filtros disponíveis
    search_fields = ('nome', 'email', 'mensagem','respondido')  # Campos de pesquisa

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)  # Campos a serem exibidos na listagem
    list_filter = ('email',)  # Filtros disponíveis
    search_fields = ('email',)  # Campos de pesquisa

admin.site.register(Contato, ContatoAdmin)
admin.site.register(Newsletter,NewsletterAdmin)
