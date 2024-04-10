from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime
import requests
from django.http import JsonResponse
from django.core.mail import send_mail

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
    def get(self, request, *args, **kwargs):                   
        return render (request, self.template )
    
