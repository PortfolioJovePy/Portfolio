from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .forms import *
from .models import *
from django.urls import resolve
from django.core.mail import send_mail
from datetime import date, datetime, timedelta
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from principal.forms import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Contatos
from django.views.decorators.csrf import csrf_exempt  # Adicionando para permitir POST
import json
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt  # Desative isso em produção e use CSRF tokens corretamente
def salvar_template(request):
    
    """Cria ou atualiza um template no banco de dados."""
    if request.method == "POST":
        nome = request.POST.get("nome")
        template = request.POST.get("template")

        if not nome or not template:
            return JsonResponse({"error": "Os campos nome e template são obrigatórios!"}, status=400)

        # Verifica se já existe um template com o mesmo nome
        obj, created = HtmlTemplate.objects.update_or_create(
            nome=nome,  # Critério de busca
            defaults={"template": template}  # Se existir, atualiza apenas o template
        )

        mensagem = "Template criado com sucesso!" if created else "Template atualizado com sucesso!"    
        
        return JsonResponse({"message": mensagem, "id": obj.id})

    return JsonResponse({"error": "Método não permitido"}, status=405)


@csrf_exempt
def salvar_contato(request):
    if request.method == 'POST':
        # Pega os dados enviados pelo AJAX
        data = json.loads(request.body)
        contato_id = data.get('id')
        nome = data.get('nome')
        email = data.get('email')
        nascimento = data.get('nascimento')
        contatos_estabelecidos = data.get('contatos_estabelecidos')
        negocios_realizados = data.get('negocios_realizados')
        faturamento = data.get('faturamento')
        lucro = data.get('lucro')

        try:
            # Atualizar o contato no banco de dados
            contato = Contatos.objects.get(id=contato_id)
            contato.nome = nome
            contato.email = email
            contato.nascimento = nascimento
            contato.contatos_estabelecidos = contatos_estabelecidos
            contato.negocios_realizados = negocios_realizados
            contato.faturamento = faturamento
            contato.lucro = lucro
            contato.save()

            return JsonResponse({'success': True})
        except Contatos.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Contato não encontrado'})

    return JsonResponse({'success': False, 'error': 'Método inválido'})

@csrf_exempt
def deletar_contato(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método inválido'})

    try:
        data = json.loads(request.body)
        contato_id = data.get('id')

        if not contato_id:
            return JsonResponse({'success': False, 'error': 'ID do contato não fornecido'})

        with transaction.atomic():  # Garante que ambas as operações sejam concluídas juntas
            # Buscar contato
            contato = Contatos.objects.get(id=contato_id)
            email = contato.email  # Capturar email antes de deletar
            contato.delete()

            # Excluir também da Newsletter, se existir
            deleted_newsletter = False
            if Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.filter(email=email).delete()
                deleted_newsletter = True

        return JsonResponse({
            'success': True,
            'message': 'Contato excluído com sucesso.',
            'newsletter_deleted': deleted_newsletter
        })

    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Contato não encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erro inesperado: {str(e)}'})



class gerenciador(LoginRequiredMixin,View):
    template = 'gerenciador.html'        
    context = {}
    def get_context(self, request, form=None):   

        if self.template == 'contatos.html':
            form = form if form is not None else ContatosForm(prefix="contatos")
            titulo = 'Informações de contato'
            submit = 'Adicionar contato'
            self.template = 'gerenciador.html'                         

        elif self.template == 'criador_template_emails.html':
            form = ''
            titulo = 'criador de template'
            submit = ''
            
        
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
                obj.enviado = True
                if obj.periodo != 'nao repete':
                    nova_data = datetime(int(obj.send_date.year), int(obj.send_date.month), int(obj.send_date.day))
                    if obj.periodo == 'diario':
                        nova_data += timedelta(days=int(obj.repeticao))
                    elif obj.periodo == 'semanal':
                        nova_data += timedelta(weeks=int(obj.repeticao))
                    elif obj.periodo == 'mensal':                        
                        novo_mes = (int(obj.send_date.month)+int(obj.repeticao))      
                        if novo_mes > 12:
                            n=0
                            while novo_mes > 12:
                                novo_mes-=12
                                n+=1
                            nova_data = datetime(int(obj.send_date.year)+n, novo_mes, int(obj.send_date.day))                                            
                        else:
                            nova_data = datetime(int(obj.send_date.year), novo_mes, int(obj.send_date.day))          
                    elif obj.periodo == 'enesimo dia util':                        
                        novo_mes = obj.send_date.month + 1
                        if novo_mes > 12:
                            novo_mes = 1
                            novo_ano = obj.send_date.year + 1
                        else:
                            novo_ano = obj.send_date.year
                        primeiro_dia_proximo_mes = datetime(novo_ano, novo_mes, 1)
                        contador_dias_uteis = 0        
                        nova_data = primeiro_dia_proximo_mes    
                        while contador_dias_uteis != int(obj.repeticao)-1:        
                            if nova_data.weekday() < 5:  
                                contador_dias_uteis += 1
                            if contador_dias_uteis != obj.repeticao:
                                nova_data += timedelta(days=1)
                            else:
                                break
                    obj.send_date = nova_data
                    obj.save()
        elif self.template == 'CRM.html':
            contatos = Contatos.objects.all()
            titulo = 'CRM'


        if self.template != 'CRM.html':            
            self.context = {'form': form, 'titulo': titulo, 'submit': submit}
        else:
            self.context = {'contatos':contatos,'titulo':titulo}
        return self.context
    

    def get(self, request, *args, **kwargs):                
        self.context = self.get_context(request)
        self.context['newsletter'] = FormularioNewsletter(idioma=request.idioma)
        return render(request, self.template, self.context)

    def post(self, request, *args, **kwargs):
        path_atual = request.path       
        self.context['newsletter'] = FormularioNewsletter
        if path_atual == '/e-mails/contatos/':
            form = ContatosForm(request.POST, prefix="contatos")
        elif path_atual == '/e-mails/agendamento/': 
            form = AgendarEmailForm(request.POST, prefix="agendar_email")            
        
        elif path_atual == '/e-mails/upload-template/': 
            form = UploadTemplateForm(request.POST, request.FILES, prefix="upload_template")                        
        elif path_atual == '/e-mails/': 
            print('teste')
        if form.is_valid():
            form.save()                 
            self.context = self.get_context(request, form=None)  
            return render(request, 'gerenciador.html', self.context)
        else:
            self.context = self.get_context(request, form=form)
            return render(request, 'gerenciador.html', self.context)