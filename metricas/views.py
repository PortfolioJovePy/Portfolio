from django.shortcuts import render, redirect
from principal.forms import *
from .forms import *
from .models import *
from django.views import View
from django.http import JsonResponse
import pandas as pd
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
            # Salva o objeto do formulário
            computarevolucao = form.save()

            # Recupera o Microobjetivo e o Objetivo de Marco
            microobjetivo = computarevolucao.objetivo
            objetivo_marco = microobjetivo.nome_objetivomarco

            # Recupera todas as notas relacionadas ao objetivo de marco
            eventos = Computarevolucao.objects.filter(objetivo__nome_objetivomarco=objetivo_marco) 
            notas = list(eventos.values_list('nota', flat=True))

            # Calcula a mediana utilizando pandas
            df = pd.DataFrame(notas, columns=['nota'])
            mediana = df['nota'].median()

            # Atualiza o status do Objetivosmarco baseado na mediana
            if mediana >= 95 and objetivo_marco.status != 'Concluído' and len(df['nota']) >= 45: #fazer teste mudando para passar no teste
                objeto_objetivo_marco = Objetivosmarco.objects.get(nome=objetivo_marco) 
                objeto_objetivo_marco.status = 'Concluído' #aqui deve mudar o valor do modelo acima, incluindo concluido                
                objeto_objetivo_marco.save()
            
            #fazer consulat equivalente para objetivos marco, buscando saber se 20% dos objetivos maroc foram atingidos

            # Redireciona para a página 'computarmetas'
            return redirect('computarmetas')

