from django.urls import path
from .views import *

urlpatterns = [
    path("", gerenciador.as_view(template='gerenciador.html'),name='gerenciador'),
    path("teste", email_teste,name='email-teste'),
]

