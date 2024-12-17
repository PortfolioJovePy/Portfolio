from django.shortcuts import render, redirect
from principal.forms import *
from .forms import *
from .models import *
from django.views import View
from django.http import JsonResponse

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
        if request.user.is_superuser:
            if self.template == 'computar.html':                 
                self.context['form_metas'] =  ComputarevolucaoForm()
                return render (request, self.template, self.context)
        else:
            return JsonResponse({
            'message': 'Fazer login para continuar. Uso restrito apenas para o dono do portfolio'
        }, status=401)
    def post(self, request, *args, **kwargs):
        form = ComputarevolucaoForm(request.POST)
        if form.is_valid():
            # Salva o objeto se o formulário for válido
            form.save()
            # Redireciona para a mesma página
            return redirect('computarmetas')

