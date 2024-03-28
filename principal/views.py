from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime
from vercel_app.settings import client
import json

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

def saudacao_com_base_no_horario():
    agora = datetime.now().time()    
    if datetime.strptime('04:30:00', '%H:%M:%S').time() <= agora < datetime.strptime('12:00:00', '%H:%M:%S').time():
        saudacao = "Bom dia"
    elif datetime.strptime('12:00:00', '%H:%M:%S').time() <= agora <= datetime.strptime('18:00:00', '%H:%M:%S').time():
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"
    return saudacao

class principal(View):
    template = 'inicio.html'
    def get(self, request, *args, **kwargs):        
        self.context = {}            
        self.context['saudacao'] = saudacao_com_base_no_horario()     
        return render (request, self.template ,self.context)