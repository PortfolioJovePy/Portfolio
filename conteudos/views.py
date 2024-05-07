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
        self.context['newsletter'] = FormularioNewsletter      
        if self.template == 'painel_conteudos.html' and request.user.is_authenticated:
            self.context['form'] = ConteudoForm()
        elif self.template == 'conteudos.html':
            self.context['conteudos'] = Conteudo.objects.all()
        elif self.template == 'e-books.html':
            self.context['form'] = FormularioLancamentoEbook1()        
        return render(request, self.template, self.context)
    
    def post(self, request):
        self.context['newsletter'] = FormularioNewsletter              
        if request.path == '/conteudos/e-books/':
            form = FormularioLancamentoEbook1(request.POST)
            if form.is_valid():
                form.save()
                self.context['titulo'] = 'Parabéns!!'
                self.context['texto'] = 'Agora você faz parte da lista de espera do meu próximo e-book. Lembrando que você foi inscrito automaticamente na minha newsletter e pode cancelar a qualquer momento.'
                try:
                    form = FormularioNewsletter(request.POST)
                    form.save()
                except:
                    pass
                return render(request,'sucesso.html',self.context)
            else:
                self.context['form'] = FormularioLancamentoEbook1(request.POST)
                return render(request, self.template, self.context)
        else:
            form = ConteudoForm(request.POST)
            if form.is_valid():            
                form.save()            
                return redirect('painel_conteudos') 
            else:
                self.context['form'] = ConteudoForm()
                return render(request, self.template, self.context)

