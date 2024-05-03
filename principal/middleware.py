from django.shortcuts import render
from datetime import datetime
from django.urls import reverse

class TempoCarregamentoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/favicon.ico':
            return self.get_response(request)        
        elif request.method == 'POST' and 'admin' not in request.path:
            request.tempo_carregamento_texto = '5s'    
            request.tempo_carregamento = 5500                        
            if '@' in request.POST['email'] and '.' in request.POST['email']:
                if len(request.POST) == 2:
                    if request.idioma == 'portugues':
                        request.texto = f'Carregando...'     
                    else:
                        request.texto = f'Loading...'     
                else:
                    if request.idioma == 'portugues':                        
                        request.texto = f'Enviando seu e-mail.'     
                    else:
                        request.texto = f'Sending your e-mail.'     
            else:
                if request.idioma == 'portugues':
                    request.texto = f'Ops! Ocorreu um problema.'
                else:
                    request.texto = f'Ops! there was a problem.'
            response = self.get_response(request)
            return response
        else:            
            if request.path == '/':
                request.tempo_carregamento_texto = '5s'    
                request.tempo_carregamento = 5500
                if request.idioma == 'portugues':
                    request.texto = f'{request.saudacao}, seja bem-vindo.'                    
                else:
                    request.texto = f'{request.saudacao}, welcome.'                    
            else:                
                request.tempo_carregamento_texto = '1.5s'    
                request.tempo_carregamento = 1500    
                if request.idioma == 'portugues':                    
                    request.texto = 'Carregando...'        
                else:
                    request.texto = 'Loading...'        
            response = self.get_response(request)
            return response

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'idioma' in request.COOKIES:
            idioma = request.COOKIES['idioma']
            if idioma == 'portugues':
                request.idioma = 'portugues'                
            else:
                request.idioma = 'ingles'
        else:
            request.idioma = 'portugues'            
        
        response = self.get_response(request)
        return response

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'theme' in request.COOKIES:
            theme = request.COOKIES['theme']
            if theme == 'dark':
                request.theme = 'dark'
                request.font = 'light'
            else:
                request.theme = 'light'
                request.font = 'dark'
        else:
            request.theme = 'dark'
            request.font = 'light'
        
        response = self.get_response(request)
        return response


class SaudacaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        agora = datetime.now().time()  # Pega o horário atual

        # Define a saudação com base no horário
        if datetime.strptime('04:30:00', '%H:%M:%S').time() <= agora < datetime.strptime('12:00:00', '%H:%M:%S').time():
            if request.idioma == 'portugues':
                saudacao = "Bom dia"
            else:
                saudacao = 'Good morning'
        elif datetime.strptime('12:00:00', '%H:%M:%S').time() <= agora <= datetime.strptime('18:00:00', '%H:%M:%S').time():
            if request.idioma == 'portugues':
                saudacao = "Boa tarde"
            else:
                saudacao = "Good afternoon"
        else:
            if request.idioma == 'portugues':
                saudacao = "Boa noite"
            else:
                saudacao = "Goodnight"
        
        # Armazena a saudação no objeto request para ser acessada mais tarde
        request.saudacao = saudacao

        response = self.get_response(request)
        return response

