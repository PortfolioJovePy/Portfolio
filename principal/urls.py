from django.urls import path
from .views import *

urlpatterns = [
    path("", principal.as_view(template='inicio.html'),name='inicio'),
    path("contato/", principal.as_view(template='contato.html'),name='contato'),
    path('toggle-theme/', toggle_theme, name='toggle-theme'),
]

