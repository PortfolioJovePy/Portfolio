from django.urls import path
from .views import *

urlpatterns = [
    path("", principal.as_view(template='inicio.html'),name='inicio'),
    path('toggle-theme/', toggle_theme, name='toggle-theme'),

]