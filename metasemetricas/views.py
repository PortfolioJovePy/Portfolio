from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from principal.forms import *

class metasemetricas(View):
    template='registroemetrica.html'
    context={}
    def get(self, request):  
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)       
        self.context['form_meta'] = MetaForm()
        self.context['form_objetivo'] = ObjetivoForm()
        self.context['form_avaliacao'] = AvaliacaoForm()
        return render(request, self.template, self.context)
    """
    def post(self, request):
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)              
        if self.template == 'e-books.html':
            form = FormularioLancamentoEbook1(request.POST)
            if form.is_valid():
                form.save()
                self.context['titulo'] = 'Parabéns!!'
                self.context['texto'] = 'Agora você faz parte da lista de espera do meu próximo e-book. Lembrando que você foi inscrito automaticamente na minha newsletter e pode cancelar a qualquer momento, basta entrar em contato comigo.'
                try:
                    form = FormularioNewsletter(request.POST,idioma=request.idioma)
                    form.save() #se acusar erro, o e-mail já existe
                except:
                    self.context['texto'] = 'Agora você faz parte da lista de espera do meu próximo e-book.'
                return render(request,'sucesso.html',self.context) #sucesso na inscrição do e-book
            else:
                self.context['form'] = FormularioLancamentoEbook1(request.POST)
                return render(request, 'e-books.html', self.context)
    """