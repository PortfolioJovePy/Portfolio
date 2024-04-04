from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .forms import *
from .models import *


class gerenciador(View):
    template = 'gerenciador.html'

    def get(self, request, *args, **kwargs):
        contatos_form = ContatosForm(prefix="contatos")
        agendar_email_form = AgendarEmailForm(prefix="agendar_email")
        return render(request, self.template, {
            'contatos_form': contatos_form,
            'agendar_email_form': agendar_email_form
        })

    def post(self, request, *args, **kwargs):
        contatos_form = ContatosForm(request.POST, prefix="contatos")
        agendar_email_form = AgendarEmailForm(request.POST, prefix="agendar_email")

        if contatos_form.is_valid() and agendar_email_form.is_valid():
            contatos_form.save()
            agendar_email_form.save()
            return redirect('inicio')  # Substitua 'nome_da_url_de_sucesso' pela URL desejada

        return render(request, self.template, {
            'contatos_form': contatos_form,
            'agendar_email_form': agendar_email_form
        })
    

def email_teste(request):
    from django.core.mail import send_mail
    send_mail(
        'Teste de E-mail',
        'Este é um e-mail de teste enviado do Django.',
        settings.EMAIL_MASK,  # Deve ser o mesmo que EMAIL_HOST_USER em settings.py
        ['r.jove@outlook.com'],  # Substitua pelo e-mail que receberá o teste
        fail_silently=False,
    )
    data = {'email':'enviado, verificar caixa'}
    return JsonResponse(data)