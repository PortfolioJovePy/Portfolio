from django import forms
from .models import *

from django import forms
from .models import *

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = avaliacao
        fields = ['objetivo', 'nota']
        widgets = {
            'objetivo': forms.Select(attrs={'class': 'form-select'}),
            'nota': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Filtrar objetivos conforme necessário
        self.fields['objetivo'].queryset = objetivos.objects.all()

class MetaForm(forms.ModelForm):
    class Meta:
        model = metas
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da meta'}),
        }

class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = objetivos
        fields = ['nome_meta', 'nome']
        widgets = {
            'nome_meta': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do objetivo'}),
        }
