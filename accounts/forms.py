from django import forms
from django.contrib.auth.models import User
from accounts.models import Doador
from .constants import UF_CHOICES

class DoadorCreateForm(forms.ModelForm):
    # Campos de usuário
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    # Campos do endereço
    cep = forms.CharField(max_length=8, required=True)
    logradouro = forms.CharField(max_length=150, required=True)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=50, required=False)
    bairro = forms.CharField(max_length=100)
    cidade = forms.CharField(max_length=100)
    estado = forms.ChoiceField(choices=UF_CHOICES)

    class Meta:
        model = Doador
        fields = ["nome", "cpf", "data_nasc", "sexo", "tipo_sang", "telefone"]
