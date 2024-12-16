from django.contrib import admin
from .models import *

# Registrando o modelo Metasdelongoprazo
@admin.register(Metasdelongoprazo)
class MetasdelongoprazoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')  # Colunas exibidas na lista
    search_fields = ('nome',)      # Permite pesquisar pelo nome no admin
    ordering = ('nome',)           # Ordena pelo nome por padrão

# Registrando o modelo Objetivosmarco
@admin.register(Objetivosmarco)
class ObjetivosmarcoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_meta', 'nome')  # Colunas exibidas na lista
    search_fields = ('nome',)                   # Permite pesquisar pelo nome no admin
    list_filter = ('nome_meta',)                 # Filtro por Meta
    ordering = ('nome_meta', 'nome')            # Ordenação por Meta e nome

@admin.register(Microobjetivos)
class MicroobjetivosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_objetivomarco', 'nome')  # Colunas exibidas na lista
    search_fields = ('nome',)                   # Permite pesquisar pelo nome no admin
    list_filter = ('nome_objetivomarco',)                 # Filtro por Meta
    ordering = ('nome_objetivomarco', 'nome')            # Ordenação por Meta e nome


# Registrando o modelo Computarevolucao
@admin.register(Computarevolucao)
class ComputarevolucaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'objetivo', 'nota', 'data')  # Colunas exibidas na lista
    search_fields = ('nota',)                           # Permite pesquisar pela nota
    list_filter = ('data',)                              # Filtro por data
    ordering = ('-data',)                                # Ordenação por data decrescente
