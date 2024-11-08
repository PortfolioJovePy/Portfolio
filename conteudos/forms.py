from django import forms
from .models import *

class ConteudoForm(forms.ModelForm):
    class Meta:
        model = Conteudo
        fields = ['titulo', 'descricao','titulo_ingles', 'descricao_ingles', 'link', 'link_imagem','link_notbook']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_ingles': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),            
            'descricao_ingles': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'link_imagem': forms.URLInput(attrs={'class': 'form-control'}),
            'link_notbook': forms.URLInput(attrs={'class': 'form-control'}),
        }



class FormularioLancamentoEbook1(forms.ModelForm):      
    class Meta:
        model = LancamentoEbook1
        fields = ['email']
        widgets = {"email": forms.EmailInput(attrs={"class":"form-control"}),}
        
        labels = {
            'email': '',
        }
        error_messages = {
            'email': {
                'unique': "Este e-mail já está cadastrado  para receber a proposta de lançamento deste e-book."
            }
        }