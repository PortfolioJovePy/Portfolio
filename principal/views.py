from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime
import requests
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import *
from django.conf import settings


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
    template = 'inicio.html'
    texto = ''    
    def get(self, request, *args, **kwargs):                   
        context = {}
        if self.template == 'inicio.html':
            if request.idioma == 'portugues':
                self.texto = f'Cientista de dados, especialista no setor imobiliário, constrói informações do zero com Python, desde a extração e estruturação de dados à insights e modelos econométricos robustos e eficientes.'            
            else:
                self.texto = f'Data scientist, specialized in the real estate sector, builds insights from scratch using Python, from data extraction and structuring to robust and efficient econometric models.'
        
        elif self.template == 'admin.html':
            pass
        context['form'] = FormularioContato(idioma=request.idioma)
        context['newsletter'] = FormularioNewsletter
        context['texto'] = self.texto
        
        return render (request, self.template, context)
    
    def post(self, request, *args, **kwargs):
        context = {}        
        if 'admin' not in (request.path):
            if len(request.POST) == 2:
                print(request.POST)
                form = FormularioNewsletter(request.POST)    
                if form.is_valid():
                    form.save()
                    if request.idioma == 'portugues':
                        context['texto'] = 'Você acaba de se inscrever na minha newsletter. Toda vez que eu publicar um novo conteúdo você será informado.'            
                        context['titulo'] = 'Parabéns!!'
                    else:
                        context['texto'] = 'You have just subscribed to my newsletter. Every time I publish new content, you will be notified.'            
                        context['titulo'] = 'Congratulations!!'
                    context['newsletter'] = FormularioNewsletter
                else:                    
                    context['texto'] = form.errors.as_text            
                    context['titulo'] = 'Ops!!'                 
                    context['newsletter'] = form                                       
                return render(request,'sucesso.html',context)
            else:
                form = FormularioContato(request.POST)
                if form.is_valid():
                    if form.cleaned_data['email']:
                        send_mail(
                                    subject='Confirmação de envio para jove.py',
                                    message=form.cleaned_data['mensagem'],                        
                                    from_email=settings.EMAIL_MASK,  
                                    recipient_list=[form.cleaned_data['email']],  
                                    fail_silently=False,
                                    #html_message =,
                                    )
                    form.save()  # Salvando os dados do formulário, assumindo que você deseja salvar
                    context['form'] = FormularioContato(idioma=request.idioma)
                    context['newsletter'] = FormularioNewsletter
                    if request.idioma == 'portugues':
                        context['texto'] = f'Que bom você me enviou uma mensagem. O responderei o mais breve possível, mas enquanto isso que tal dar uma olhada nos meus conteúdos e e-books.'    
                        context['titulo'] = 'Seu e-mail foi enviado!'
                    else:
                        context['texto'] = f"How nice of you to send me a message. I'll get back to you as soon as possible, but in the meantime, why not take a look at my content and e-books."
                        context['titulo'] = f"Your email has been sent!"
                    
                    return render(request,'sucesso.html',context)
                    
                else:        
                    context['form'] = form            
                    context['newsletter'] = FormularioNewsletter
                    if request.idioma == 'portugues':                        
                        context['texto'] = f'Parece que o formulário foi preenchido incorretamente. Por favor, verifique os dados informados.'    
                    else:
                        context['texto'] = "It looks like the form was filled out incorrectly. Please check the information provided."
                    context['titulo'] = 'Ops!'                    
            return render(request, self.template, context)