from django.contrib import admin

from django.contrib import admin
from .models import *

class ObjetivoInline(admin.TabularInline):
    model = objetivos
    extra = 1

@admin.register(metas)
class MetaAdmin(admin.ModelAdmin):
    inlines = [ObjetivoInline]

@admin.register(objetivos)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nome_meta']

@admin.register(avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['objetivo', 'nota', 'data']
