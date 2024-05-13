from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from principal.forms import *

class painel_conteudos(View):
    template='painel_conteudos.html'
    context={}
    def get(self, request):  
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)
        
        if self.template == 'painel_conteudos.html' and request.user.is_authenticated:
            self.context['form'] = ConteudoForm()
        
        
        elif self.template == 'conteudos.html':
            self.context['conteudos'] = reversed(list(Conteudo.objects.all()))
        
        elif self.template == 'e-books.html':
            self.context['form'] = FormularioLancamentoEbook1()        
        
        
        return render(request, self.template, self.context)
    
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
        
        elif self.template == 'painel_conteudos.html':
            form = ConteudoForm(request.POST)
            if form.is_valid():            
                form.save()            
                return redirect('painel_conteudos') 
            else:
                self.context['form'] = form #retorna o formulário com erro
                return render(request, 'painel_conteudos.html', self.context)

