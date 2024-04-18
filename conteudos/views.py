from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ConteudoForm
from .models import Conteudo

class painel_conteudos(LoginRequiredMixin,View):
    template='painel_conteudos.html'
    context={}
    def get(self, request):        
        if self.template == 'painel_conteudos.html':
            self.context['form'] = ConteudoForm()
        elif self.template == 'conteudos.html':
            self.context['conteudos'] = Conteudo.objects.all()
        return render(request, self.template, self.context)
    
    def post(self, request):
        form = ConteudoForm(request.POST)
        if form.is_valid():            
            form.save()            
            return redirect('painel_conteudos') 
        else:
            self.context['form'] = ConteudoForm()
            return render(request, self.template, self.context)

