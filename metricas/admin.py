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

    def get_search_results(self, request, queryset, search_term):
        # Sobrescrevendo o método para garantir que ele retorna 2 valores
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term)
        
        # Adicione ou modifique qualquer lógica de busca que desejar
        return queryset, may_have_duplicates  # Retornando exatamente dois valores

@admin.register(Microobjetivos)
class MicroobjetivosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_objetivomarco', 'nome')  # Colunas exibidas na lista
    search_fields = ('nome',)                           # Permite pesquisar pelo nome no admin
    list_filter = ('nome_objetivomarco',)               # Filtro por ObjetivoMarco
    ordering = ('nome_objetivomarco', 'nome')           # Ordenação por ObjetivoMarco e nome

    # Exibindo o nome do objetivo relacionado
    def nome_objetivomarco(self, obj):
        return obj.nome_objetivomarco.nome  # Exibe o nome do objetivo relacionado
    nome_objetivomarco.admin_order_field = 'nome_objetivomarco__nome'

# Registrando o modelo Computarevolucao
@admin.register(Computarevolucao)
class ComputarevolucaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'objetivo', 'nota', 'data')  # Colunas exibidas na lista
    search_fields = ('nota',)                           # Permite pesquisar pela nota
    list_filter = ('data',)                              # Filtro por data
    ordering = ('-data',)                                # Ordenação por data decrescente

    # Exibindo o nome do objetivo relacionado
    def objetivo(self, obj):
        return obj.objetivo.nome  # Exibe o nome do microobjetivo relacionado
    objetivo.admin_order_field = 'objetivo'  # Permite ordenar por objetivo
