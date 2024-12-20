from django.urls import path
from .views import *

urlpatterns = [
    path("", minhasmetas.as_view(template='computar.html'),name='computarmetas'),    
    path("visao-geral/", minhasmetas.as_view(template='visao_geral.html'),name='visao-geral')    
]

