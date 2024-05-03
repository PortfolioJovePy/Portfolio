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
            self.texto = f'Cientista de dados, especialista no setor imobiliário, constrói informações do zero com Python, desde a extração e estruturação de dados à insights e modelos econométricos robustos e eficientes.'            
        context['form'] = FormularioContato
        context['newsletter'] = Newsletter
        context['texto'] = self.texto
        context['titulo'] = 'Sobre'
        
        return render (request, self.template, context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        print(len(request.POST),(request.POST))
        if len(request.POST) == 2:
            form = Newsletter(request.POST)    
            form.save()
            return redirect('sucesso')
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
                context['form'] = FormularioContato
                context['newsletter'] = Newsletter
                context['texto'] = f'Que bom você me enviou uma mensagem. O responderei o mais breve possível, mas enquanto isso que tal dar uma olhada nos meus conteúdos e e-books'    
                context['titulo'] = 'Seu e-mail foi enviado!'
                return redirect('sucesso')
                
            else:        
                context['form'] = form            
                context['texto'] = f'Parece que o formulário foi preenchido incorretamente. Por favor, verifique os dados informados'    
                context['titulo'] = 'Ops!'
        return render(request, self.template, context)