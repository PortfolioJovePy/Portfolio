from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class painel_conteudos(LoginRequiredMixin,View):
    template='painel_conteudos.html'
    def get(self, request):
        # Aqui você pode incluir qualquer lógica que precisar para processar a requisição GET
        return HttpResponse("Olá, mundo! Esta é a resposta do método GET.")
