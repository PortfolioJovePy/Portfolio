from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *

class painel_conteudos(View):
    template='painel_conteudos.html'
    context={}
    def get(self, request):        
        if self.template == 'painel_conteudos.html' and request.user.is_authenticated:
            self.context['form'] = ConteudoForm()
        elif self.template == 'conteudos.html':
            self.context['conteudos'] = Conteudo.objects.all()
        elif self.template == 'e-books.html':
            self.context['form'] = FormularioLancamentoEbook1()        
        return render(request, self.template, self.context)
    
    def post(self, request):
        print(request.path)
        if request.path == '/conteudos/e-books/':
            form = FormularioLancamentoEbook1(request.POST)
            if form.is_valid():
                form.save()
                return redirect('sucesso')
            else:
                self.context['form'] = ConteudoForm()
                return render(request, self.template, self.context)
        else:
            form = ConteudoForm(request.POST)
            if form.is_valid():            
                form.save()            
                return redirect('painel_conteudos') 
            else:
                self.context['form'] = ConteudoForm()
                return render(request, self.template, self.context)

