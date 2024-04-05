from django import forms
from .models import *

class ContatosForm(forms.ModelForm):
    class Meta:
        model = Contatos
        fields = ['nome', 'email', 'nascimento', 'contatos_estabelecidos', 'negocios_realizados']
        labels = {
            'nome': 'Nome',
            'email': 'E-mail',
            'nascimento': 'Data de Nascimento',
            'contatos_estabelecidos': 'Contatos Estabelecidos',
            'negocios_realizados': 'Negócios Realizados',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nascimento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'contatos_estabelecidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'negocios_realizados': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AgendarEmailForm(forms.ModelForm):
    class Meta:
        model = AgendarEmail
        fields = ['nome', 'send_date', 'send_time', 'email_template', 'enviado']
        widgets = {
            'nome': forms.Select(attrs={'class': 'form-control'}),
            'send_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
            'send_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'email_template': forms.Textarea(attrs={'class': 'form-control'}),
            'enviado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UploadTemplateForm(forms.ModelForm):
    class Meta:
        model = UploadTemplate
        fields = ['nome', 'arquivo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Arquivo'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


