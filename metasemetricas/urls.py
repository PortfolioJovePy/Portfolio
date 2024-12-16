from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path("", metasemetricas.as_view(template='registrometrica.html'),name='registro-diario'),      
]

