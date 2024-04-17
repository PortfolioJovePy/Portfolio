from django.urls import path
from .views import *

urlpatterns = [
    path("", principal.as_view(template='inicio.html'),name='inicio'),
    path("sobre/", principal.as_view(template='sobre.html'),name='sobre'),
    path('toggle-theme/', toggle_theme, name='toggle-theme'),
]

