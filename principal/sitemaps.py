from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class PrincipalSitemap(Sitemap):
    changefreq = "weekly"  # Frequência de atualização
    priority = 0.5         # Prioridade relativa

    def items(self):
        # Retorna as páginas disponíveis associadas à view `principal`
        return ['inicio','sobre', 'sucesso', 'CV']

    def location(self, item):
        # Mapeia os itens para suas URLs
        return reverse(item)
