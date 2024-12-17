from django.shortcuts import render
from principal.forms import *
from django.views import View

# Create your views here.
class minhasmetas(View):
    """
    Classe principal do site. Local onde páginas básicas se encontrarão, sem dinâmica ou implementação. Informação pura.
    """
    template = 'computar.html'        
    context={}
    #@method_decorator(cache_page(60 * 60))
    def get(self, request, *args, **kwargs):                           
        self.context = {}
        #Trecho para formulários básicos sempre necessários ao GET
        self.context['form'] = FormularioContato(idioma=request.idioma)
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)                
        #Trecho de páginas específicas
        if self.template == 'computar.html':     
            return render (request, self.template, self.context)

