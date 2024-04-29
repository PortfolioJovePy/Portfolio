from django import forms
from .models import Contato

class FormularioContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control mb-2','placeholder': 'Apresente-se'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'E-mail'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control mb-2', 'placeholder': 'Sobre o que você quer conversar?', 'rows': 6}),
        }
        labels = {
            'nome': '',
            'email': '',
            'mensagem': ''
        }
