from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from .models import Visitantes
from bs4 import BeautifulSoup
import requests

class CalculoTempoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):     
        if 'favicon' in request.path or 'estaticos' in request.path:
            return self.get_response(request)        
        else:
            if 'entrada' not in request.session:
                # Se não houver entrada na sessão, cria uma nova entrada com o tempo atual
                request.session['entrada'] = str(timezone.now())
            
            response = self.get_response(request)
            hoje = timezone.now().date()
            visitante_do_dia = Visitantes.objects.filter(data=hoje).first()
            entrada_str = request.session['entrada']
            entrada = datetime.strptime(entrada_str, "%Y-%m-%d %H:%M:%S.%f%z")                            
            saida = timezone.now()
            tempo_sessao = saida - entrada
            
            if visitante_do_dia:                                            
                if entrada != visitante_do_dia.entrada:
                    visitante_do_dia.entrada = entrada                                                            
                    visitante_do_dia.tempo_sessao += tempo_sessao #adiciona o tempo                    
                    print('Tempo de sessao somado t0+t1')
                else:
                    if visitante_do_dia.tempo_sessao > tempo_sessao: #se no calculo a sessao for menor q o total, adiciona-se
                        visitante_do_dia.tempo_sessao += tempo_sessao
                        print('Tempo de sessao somado t0+t1 onde t0>t1')
                    else:                    
                        visitante_do_dia.tempo_sessao = tempo_sessao #assume um erro de calculo e coloca o tempo superior no local da sessao
                        print('Tempo de sessao somado t0<-t1 onde t0<t1')
                visitante_do_dia.save()
                request.session['entrada'] = str(timezone.now()) #evita caso uma nova requisicao seja feita
                print('o novo tempo de entrada é',request.session['entrada'])
                print('Tempo de sessão computado',tempo_sessao)
            else:
                # Se não existe, cria um novo objeto Visitantes para o dia atual
                try:
                    ip = request.META['REMOTE_ADDR']
                    url =f'https://www.geolocation.com/pt?ip={ip}#ipresult'
                    r = requests.get(url)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    
                    infos_ip = soup.find('table').find_all('td')                    
                    visitante = Visitantes.objects.create(
                        ip=ip,
                        data=hoje,
                        entrada =  timezone.now(),
                        saida = saida,
                        tempo_sessao=tempo_sessao,
                        pais=infos_ip[1].text,
                        regiao=infos_ip[2].text,
                        cidade=infos_ip[3].text,
                    )
                    visitante.save()
                except Exception as e:
                    print(e)
                
            
            return response

class TempoCarregamentoMiddleware:    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):        
        if 'favicon' in request.path or 'estaticos' in request.path:
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

