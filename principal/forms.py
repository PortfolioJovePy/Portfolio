from django import forms
from .models import Contato

class FormularioContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }
        labels = {
            'nome': 'Apresente-se',
            'email': 'E-mail',
            'mensagem': 'Sobre o que você quer conversar?'
        }
