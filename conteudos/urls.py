from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", painel_conteudos.as_view(template='painel_conteudos.html'),name='painel_conteudos'),    
    path("", painel_conteudos.as_view(template='conteudos.html'),name='conteudos'),    
]

