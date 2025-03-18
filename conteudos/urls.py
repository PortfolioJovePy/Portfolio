from django.urls import path
from .views import *



urlpatterns = [
    path("admin/conteudos/", painel_conteudos.as_view(template='painel_conteudos.html'),name='painel_conteudos'),    
    path("admin/leituras/", painel_conteudos.as_view(template='painel_conteudos.html'),name='painel_leituras'),
    path("admin/ebooks/", painel_conteudos.as_view(template='painel_conteudos.html'),name='painel_ebooks'),    
    path("publicacoes/", painel_conteudos.as_view(template='conteudos.html'),name='publicações'),    
    path("e-books/", painel_conteudos.as_view(template='e-books.html'),name='ebooks'),  
    path("leituras-recomendadas/", painel_conteudos.as_view(template='leituras_recomendadas.html'),name='leituras_recomendadas'),    

]


