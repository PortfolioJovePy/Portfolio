from django.urls import path
from .views import *

urlpatterns = [
    path("", principal.as_view(template='inicio.html'),name='inicio'),
    path("sobre/", principal.as_view(template='sobre.html'),name='sobre'),
    path("sucesso/", principal.as_view(template='sucesso.html'),name='sucesso'),
    path("painel-do-administrador/", principal.as_view(template='admin.html'),name='painel-do-administrador'),
    path('toggle-theme/', toggle_theme, name='toggle-theme'),
]

