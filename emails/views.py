from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .forms import *
from .models import *
from django.urls import resolve

class gerenciador(View):
    template = 'gerenciador.html'
    
    def get_context(self, request, form=None):
        if self.template == 'contatos.html':
            form = form if form is not None else ContatosForm(prefix="contatos")
            titulo = 'Informações de contato'
            submit = 'Adicionar contato'
        elif self.template == 'agendamento.html':
            form = form if form is not None else AgendarEmailForm(prefix="agendar_email")
            titulo = 'Agendamento de e-mail'
            submit = 'Agendar e-mail'
        elif self.template == 'upload_template.html':
            form = form if form is not None else UploadTemplateForm(prefix="upload_template")
            titulo = 'Cadastro de modelos de templates de e-mail'
            submit = 'Incluir template'

        context = {'form': form, 'titulo': titulo, 'submit': submit}
        return context
    
    def get(self, request, *args, **kwargs):        
        context = self.get_context(request)
        return render(request, 'gerenciador.html', context)

    def post(self, request, *args, **kwargs):
        path_atual = request.path       
        if path_atual == '/e-mails/contatos/':
            form = ContatosForm(request.POST, prefix="contatos")
        elif path_atual == '/e-mails/agendamento/': 
            form = AgendarEmailForm(request.POST, prefix="agendar_email")            
        
        elif path_atual == '/e-mails/upload-template/': 
            form = UploadTemplateForm(request.POST, request.FILES, prefix="upload_template")            
            print(form)
        
        if form.is_valid():
            form.save()            
            context = self.get_context(request, form=None)  
            return render(request, 'gerenciador.html', context)
        else:
            context = self.get_context(request, form=form)
            return render(request, 'gerenciador.html', context)

    

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