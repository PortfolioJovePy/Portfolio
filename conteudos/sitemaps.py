from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Conteudo, Leituras, Ebooks

class ConteudoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Conteudo.objects.all()

    def location(self, obj):
        return reverse('publicações')  # Usa a URL nomeada correspondente

class LeiturasSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Leituras.objects.all()

    def location(self, obj):
        return reverse('leituras_recomendadas')

class EbooksSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Ebooks.objects.all()

    def location(self, obj):
        return reverse('ebooks')
