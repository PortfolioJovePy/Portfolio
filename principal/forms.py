from django import forms
from .models import Contato

class FormularioContato(forms.ModelForm):
    def __init__(self, *args, font_class='', **kwargs):
        super(FormularioContato, self).__init__(*args, **kwargs)
        # Adiciona a classe font dinamicamente
        classes_base = 'form-control mb-2'
        self.fields['nome'].widget.attrs['class'] = f"{classes_base} {font_class}"
        self.fields['email'].widget.attrs['class'] = f"{classes_base} {font_class}"
        self.fields['mensagem'].widget.attrs['class'] = f"{classes_base} {font_class}"
        
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
