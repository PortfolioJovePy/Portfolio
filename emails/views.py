from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .forms import *
from .models import *
from django.urls import resolve
from django.core.mail import send_mail
from datetime import date
from django.conf import settings
from django.shortcuts import get_object_or_404


class gerenciador(View):
    template = 'gerenciador.html'
    
    def get_context(self, request, form=None):
        if self.template == 'contatos.html':
            form = form if form is not None else ContatosForm(prefix="contatos")
            titulo = 'Informações de contato'
            submit = 'Adicionar contato'
            self.template = 'gerenciador.html'
        
        elif self.template == 'agendamento.html':
            form = form if form is not None else AgendarEmailForm(prefix="agendar_email")
            titulo = 'Agendamento de e-mail'
            submit = 'Agendar e-mail'
            self.template = 'gerenciador.html'
        
        elif self.template == 'upload_template.html':
            form = form if form is not None else UploadTemplateForm(prefix="upload_template")
            titulo = 'Cadastro de modelos de templates de e-mail'
            submit = 'Incluir template'
            self.template = 'gerenciador.html'
        
        elif self.template == 'painel.html':
            form = form if form is not None else UploadTemplateForm(prefix="upload_template")
            titulo = 'Painel de controle dos e-mails'
            submit = 'Incluir template'
            emails = AgendarEmail.objects.filter(enviado=False,send_date=date.today())
            for obj in emails:
                with open(f'./media/uploads_html/{obj.email_template}.html', 'r', encoding='utf-8') as f:
                    conteudo = f.read()          
                send_mail(
                        subject=obj.assunto,
                        message='Caso não visualize este email abra-o em um cliente compatível com HTML para ver a versão completa.',                        
                        from_email=settings.EMAIL_MASK,  
                        recipient_list=[obj.email],  
                        fail_silently=False,
                        html_message =conteudo,
                        )
                #APOS ENVIO FAZER UPDATE PARA ENVIADO = TRUE                


        context = {'form': form, 'titulo': titulo, 'submit': submit}
        return context
    
    def get(self, request, *args, **kwargs):                
        context = self.get_context(request)
        return render(request, self.template, context)

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
    data = {'email':'enviado, verificar caixa'}
    return JsonResponse(data)