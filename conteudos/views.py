from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from principal.forms import *
from emails.models import Contatos

def criar_contato(nome, email, nascimento, contatos_estabelecidos, negocios_realizados,faturamento,lucro):
    try:
        if not Contatos.objects.filter(email=email).exists():
            contato = Contatos.objects.create(
                nome=nome,
                email=email,
                nascimento=nascimento,
                contatos_estabelecidos=contatos_estabelecidos,
                negocios_realizados=negocios_realizados,
                faturamento=faturamento,
                lucro=lucro
            )
            return contato    
        return None  # Retorna None caso o e-mail já exista
    except Exception as e:
        print(e)


class painel_conteudos(View):
    template='conteudos.html'
    context={}
    #@method_decorator(cache_page(60 * 60))
    def get(self, request):  
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)
        
        if self.template == 'painel_conteudos.html' and request.user.is_authenticated:
            if 'conteudos' in request.path:
                self.context['form'] = ConteudoForm()
            elif 'e-books' in request.path:
                self.context['form'] = EbooksForm()
            else:
                self.context['form'] = LeiturasForm()
        
        
        elif self.template == 'conteudos.html':                    
            self.context['conteudos'] = reversed(list(Conteudo.objects.all().order_by('id')))
        
        elif self.template == 'e-books.html':
            self.context['form'] = FormularioLancamentoEbook1()        
            self.context['conteudos'] = reversed(list(Ebooks.objects.all().order_by('id')))

        elif self.template == 'leituras_recomendadas.html':                    
            self.context['conteudos'] = reversed(list(Leituras.objects.all().order_by('id')))
        
        
        return render(request, self.template, self.context)
    
    def post(self, request):
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)              
        if self.template == 'e-books.html':
            form = FormularioLancamentoEbook1(request.POST)
            if form.is_valid():
                form.save()
                criar_contato('Não consta',form.cleaned_data['email'],'Não consta',0,0,0,0)
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
            if 'conteudos' in request.path:
                form = ConteudoForm(request.POST)
            else:
                form = LeiturasForm(request.POST)
            if form.is_valid():            
                form.save()            
                return redirect('painel_conteudos') 
            else:
                self.context['form'] = form #retorna o formulário com erro
                return render(request, 'painel_conteudos.html', self.context)

