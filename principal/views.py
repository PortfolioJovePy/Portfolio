from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime
import requests
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import FormularioContato
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
            self.texto = f'{request.saudacao}, tudo bom?&&Seja muito bem-vindo.&&É um prazer tê-lo aqui.'            
        elif self.template == 'contato.html':
            pass
        context['form'] = FormularioContato
        context['texto'] = self.texto
        return render (request, self.template, context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        form = FormularioContato(request.POST)
        if form.is_valid():
            # Aqui você pode adicionar lógica para salvar o formulário ou enviar um e-mail, etc.
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
            context['texto'] = f'{request.saudacao}, seu email foi enviado com sucesso.&&Você recebeu um e-mail de confirmação.'
            return render(request, 'inicio.html', context)
        else:        
            context['form'] = form
            return render(request, self.template, context)