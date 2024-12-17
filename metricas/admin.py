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

    # Adicionando exibição mais detalhada para a relação
    def nome_meta(self, obj):
        return obj.nome_meta.nome  # Exibe o nome da meta, não o objeto em si
    nome_meta.admin_order_field = 'nome_meta'  # Permite ordenar por nome_meta
    
    # Adicionando filtros para uma melhor visualização no Admin
    def get_search_results(self, request, queryset, search_term):
        # Sobrescrevendo a pesquisa para incluir as opções de 'nome_meta' no campo de filtro
        return queryset.filter(nome__icontains=search_term)

    # Adicionando inline para exibição relacionada
    inlines = [
        # Adiciona as opções de inserção relacionadas, se necessário
    ]

@admin.register(Microobjetivos)
class MicroobjetivosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_objetivomarco', 'nome')  # Colunas exibidas na lista
    search_fields = ('nome',)                   # Permite pesquisar pelo nome no admin
    list_filter = ('nome_objetivomarco',)       # Filtro por ObjetivoMarco
    ordering = ('nome_objetivomarco', 'nome')    # Ordenação por ObjetivoMarco e nome

    # Exibindo o nome do objetivo relacionado
    def nome_objetivomarco(self, obj):
        return obj.nome_objetivomarco.nome  # Exibe o nome do objetivo relacionado
    nome_objetivomarco.admin_order_field = 'nome_objetivomarco'  # Permite ordenar por nome_objetivomarco

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
