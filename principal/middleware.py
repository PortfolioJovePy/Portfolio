from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from .models import Visitantes
from bs4 import BeautifulSoup
import requests
import re
from django.http import HttpResponse


class CalculoTempoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):             
        if 'favicon' in request.path or 'static' in request.path or 'robots' in request.path or 'script' in request.path:
            print("Se carregar duas vezes, investigar bug aqui")
            pass

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
                else:
                    if visitante_do_dia.tempo_sessao > tempo_sessao: #se no calculo a sessao for menor q o total, adiciona-se
                        visitante_do_dia.tempo_sessao += tempo_sessao
                    else:                    
                        visitante_do_dia.tempo_sessao = tempo_sessao #assume um erro de calculo e coloca o tempo superior no local da sessao                        
                visitante_do_dia.save()
                request.session['entrada'] = str(timezone.now()) #evita caso uma nova requisicao seja feita
            else:
                # Se não existe, cria um novo objeto Visitantes para o dia atual
                try:
                    ip = request.META['REMOTE_ADDR']
                    url =f'https://www.geolocation.com/pt?ip={ip}#ipresult'
                    r = requests.get(url)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    
                    infos_ip = soup.find('table').find_all('td')                        
                    
                    pais= re.sub(r'\s+', ' ', infos_ip[1].text.replace('\n',' '))
                    regiao= re.sub(r'\s+', ' ', infos_ip[2].text.replace('\n',' '))
                    cidade= re.sub(r'\s+', ' ', infos_ip[3].text.replace('\n',' '))

                    visitante = Visitantes.objects.create(
                        ip=ip,
                        data=hoje,
                        entrada =  timezone.now(),
                        saida = saida,
                        tempo_sessao=tempo_sessao,
                        pais=pais,
                        regiao=regiao,
                        cidade=cidade,
                    )
                    visitante.save()
                except Exception as e:
                    print(e)
                
            
            return response

class TempoCarregamentoMiddleware:    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):      
        if 'favicon' in request.path or 'staticfiles' in request.path  or 'particles' in request.path or 'static' in request.path or '.png' in request.path:
            return HttpResponse()

        elif request.method == 'POST' and 'admin' not in request.path and 'e-mails' not in request.path and 'metas' not in request.path:
            request.tempo_carregamento_texto = '.4s'    
            request.tempo_carregamento = 400                        
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
                request.tempo_carregamento_texto = '.8s'    
                request.tempo_carregamento = 800
                if request.idioma == 'portugues':
                    request.texto = f'{request.saudacao}, seja bem-vindo.'                    
                else:
                    request.texto = f'{request.saudacao}, welcome.'                    
            else:                
                request.tempo_carregamento_texto = '.4s'    
                request.tempo_carregamento = 400    
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

