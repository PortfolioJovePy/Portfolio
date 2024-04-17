from django.urls import path
from .views import *

urlpatterns = [
    path("", painel_conteudos.as_view(template='painel.html'),name='painel_conteudos'),    
]

