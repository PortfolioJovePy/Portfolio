
from conteudos.models import *


from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime
import requests
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import *
from django.conf import settings
from django.utils import timezone


def toggle_theme(request):
    current_theme = request.COOKIES.get('theme', 'dark')
    new_theme = 'dark' if current_theme == 'light' else 'light'    
    referer = request.META.get('HTTP_REFERER') or '/'    
    response = redirect(referer)
    response.set_cookie('theme', new_theme)
    return response


def portugues(request):    
    referer = request.META.get('HTTP_REFERER') or '/'    
    response = redirect(referer)
    response.set_cookie('idioma', 'portugues')
    return response

def ingles(request):    
    referer = request.META.get('HTTP_REFERER') or '/'    
    response = redirect(referer)
    response.set_cookie('idioma', 'ingles')
    return response


def error(request, exception):   
    error_code = getattr(exception, 'status_code', 500)
    context = {'error':f'Erro n.º {error_code}  '}
    return render(request, 'error.html',context, status=error_code)



class principal(View):
    """
    Classe principal do site. Local onde páginas básicas se encontrarão, sem dinâmica ou implementação. Informação pura.
    """
    template = 'inicio.html'
    texto = ''    
    context={}
    #@method_decorator(cache_page(60 * 60))
    def get(self, request, *args, **kwargs):                           

        self.context = {}
        #Trecho para formulários básicos sempre necessários ao GET
        self.context['form'] = FormularioContato(idioma=request.idioma)
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)        
        
        #Trecho de páginas específicas
        if self.template == 'inicio.html':
            self.titulo = 'Rodrigo Jovê'
            if request.idioma == 'portugues':
                self.texto = f'Economista, com 5 anos de experiência no setor imobiliário, constrói informações do zero com Python, desde a extração e estruturação de dados à insights e modelos econométricos robustos e eficientes.'            
            else:
                self.texto = f'Economist with 5 years of experience in the real estate sector, skilled in building information from scratch with Python, from data extraction and structuring to generating insights and developing robust and efficient econometric models.'
            self.context['titulo'] = self.titulo
            self.context['texto'] = self.texto                            
            self.context['conteudos'] = self.context['conteudos'] = reversed(list(Conteudo.objects.all().order_by('id'))[-3:])


        elif self.template == 'admin.html':
            if not request.user.is_superuser:
                return redirect ('inicio') #não permite usuarios de modo algum o request de admin
                
        elif self.template == 'sucesso.html':
            return redirect ('inicio') #não permite o get direto de sucesso

        
        return render (request, self.template, self.context)



    def post(self, request, *args, **kwargs):
        self.context = {}        
        self.context['form'] = FormularioContato(idioma=request.idioma)
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)                
        if 'admin' not in (request.path) or 'upload-template/' not in (request.path): #POST de usuário público

            #formulário de contato
            if 'nome' in request.POST.keys() and 'inicio.html' in self.template:
                form = FormularioContato(request.POST)
                if form.is_valid():
                    if form.cleaned_data['email']:
                        send_mail(
                                    subject='Confirmação de envio para jove.py',
                                    message=form.cleaned_data['mensagem'],                        
                                    from_email=settings.EMAIL_MASK,  
                                    recipient_list=[form.cleaned_data['email'],settings.EMAIL_MASK],  
                                    fail_silently=False,
                                    )
                    form.save() 
                    if request.idioma == 'portugues':
                        self.context['texto'] = f'Que bom você me enviou uma mensagem. O responderei o mais breve possível, mas enquanto isso que tal dar uma olhada nos meus conteúdos e e-books.'    
                        self.context['titulo'] = 'Seu e-mail foi enviado!'
                    else:
                        self.context['texto'] = f"How nice of you to send me a message. I'll get back to you as soon as possible, but in the meantime, why not take a look at my content and e-books."
                        self.context['titulo'] = f"Your email has been sent!"
                    
                    return render(request,'sucesso.html',self.context) #sucesso no envio do email
                    
                else:        
                    self.context['titulo'] = 'Ops!!!'
                    self.context['form'] = form #retorna formulári com erros                                
                    
                    if request.idioma == 'portugues':                        
                        self.context['texto'] = f'Parece que o formulário foi preenchido incorretamente. Por favor, verifique os dados informados.'    
                    else:
                        self.context['texto'] = "It looks like the form was filled out incorrectly. Please check the information provided."
                    
                    return render(request,'inicio.html',self.context)               
                
            #formulário newsletter     
            else:  
                form = FormularioNewsletter(request.POST,idioma=request.idioma)    
                if form.is_valid():
                    form.save()
                    if request.idioma == 'portugues':
                        self.context['texto'] = 'Você acaba de se inscrever na minha newsletter. Toda vez que eu publicar um novo conteúdo você será informado.'            
                        self.context['titulo'] = 'Parabéns!!'
                    else:
                        self.context['texto'] = 'You have just subscribed to my newsletter. Every time I publish new content, you will be notified.'            
                        self.context['titulo'] = 'Congratulations!!'
                    self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)
                    return render(request,'sucesso.html',self.context) #sucesso de cadastro de email
                
                else:  #fracasso no formulário. Reexibe a tela atual.
                    self.context['texto'] = form.errors.as_text            
                    self.context['titulo'] = 'Ops!!'                 
                    self.context['newsletter'] = form                                               
                    return render(request,'inicio.html',self.context)
            