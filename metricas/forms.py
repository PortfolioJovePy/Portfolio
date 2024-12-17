from django import forms
from .models import *

class ComputarevolucaoForm(forms.ModelForm):
    class Meta:
        model = Computarevolucao
        fields = ['objetivo', 'nota']
        
        widgets = {
            'objetivo': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Selecione um objetivo'
            }),
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1, 
                'max': 100, 
                'step': 1,
                'placeholder': 'Nota de 1 a 100',
                'title': 'Informe uma nota entre 1 e 100'
            }),
        }
        
        labels = {
            'objetivo': 'Objetivo',
            'nota': 'Nota',
        }

        help_texts = {
            'nota': 'Atribua uma nota de 1 a 100 para o objetivo.',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aceitar parâmetros adicionais para filtrar objetivos
        self.fields['objetivo'].queryset = Microobjetivos.objects.all()

        # Adicionar classes CSS ou outros atributos ao select
        self.fields['objetivo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Selecione um objetivo correspondente'
        })
