from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PrincipalSitemap

sitemaps = {
    'principal': PrincipalSitemap,
}
urlpatterns = [
    path("", principal.as_view(template='inicio.html'),name='inicio'),
    path("sobre/", principal.as_view(template='sobre.html'),name='sobre'),
    path("sucesso/", principal.as_view(template='sucesso.html'),name='sucesso'),
    path("painel-do-administrador/", principal.as_view(template='admin.html'),name='painel-do-administrador'),
    path('toggle-theme/', toggle_theme, name='toggle-theme'),
    path('portugues/', portugues, name='portugues'),
    path('ingles/', ingles, name='ingles'),
    path('CV/', principal.as_view(template='CV.html'), name='CV'),
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps},name="django.contrib.sitemaps.views.sitemap"),
    path("assistenterodrigo", assistenterodrigo, name="assistenterodrigo"),    
]

