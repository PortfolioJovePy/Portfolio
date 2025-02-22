from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import logging
from django.conf import settings

# Configuração de logs
logger = logging.getLogger(__name__)

# Tokens e Configurações
GRAPH_API_TOKEN = settings.GRAPH_API_TOKEN  # Defina isso no settings.py
WEBHOOK_VERIFY_TOKEN = settings.WEBHOOK_VERIFY_TOKEN  # Defina isso no settings.py
BUSINESS_PHONE_NUMBER_ID = settings.BUSINESS_PHONE_NUMBER_ID  # Defina no settings.py

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        print('aqui')
        """Verificação inicial do Webhook com Meta API"""
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
            logger.info("Webhook verificado com sucesso!")
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("Erro na verificação", status=403)

    elif request.method == "POST":
        """Processa mensagens recebidas do WhatsApp"""
        try:
            data = json.loads(request.body)
            logger.info(f"Webhook recebido: {json.dumps(data, indent=2)}")

            if "entry" in data:
                for entry in data["entry"]:
                    for change in entry.get("changes", []):
                        if "value" in change and "messages" in change["value"]:
                            messages = change["value"]["messages"]
                            for message in messages:
                                processar_mensagem(message)
            
            return JsonResponse({"status": "sucesso"}, status=200)

        except Exception as e:
            logger.error(f"Erro ao processar webhook: {str(e)}")
            return JsonResponse({"error": "Erro ao processar webhook"}, status=500)

    return JsonResponse({"error": "Método não permitido"}, status=405)

def processar_mensagem(message):
    """Processa as mensagens e marca como lidas"""
    numero = message["from"]
    message_id = message["id"]
    tipo_mensagem = message["type"]

    logger.info(f"Mensagem recebida de {numero}: {message}")

    # Marcar a mensagem como lida
    marcar_mensagem_como_lida(message_id)

    if tipo_mensagem == "text":
        texto = message["text"]["body"]
        logger.info(f"Texto recebido: {texto}")
    
    elif tipo_mensagem == "image":
        imagem_url = message["image"]["link"]
        logger.info(f"Imagem recebida: {imagem_url}")
    
    elif tipo_mensagem == "audio":
        audio_url = message["audio"]["link"]
        logger.info(f"Áudio recebido: {audio_url}")
    
    else:
        logger.info(f"Tipo de mensagem não suportado: {tipo_mensagem}")

def marcar_mensagem_como_lida(message_id):
    """Envia requisição para marcar a mensagem como lida"""
    url = f"https://graph.facebook.com/v18.0/{BUSINESS_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {GRAPH_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        logger.info(f"Mensagem {message_id} marcada como lida.")
    else:
        logger.error(f"Erro ao marcar mensagem como lida: {response.text}")
