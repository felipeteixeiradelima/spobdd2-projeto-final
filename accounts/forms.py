from re import sub
from django import forms
from django.contrib.auth.models import User
from accounts.models import Doador, Endereco

class DoadorCreateForm(forms.ModelForm):
    # Campos de usuário
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    # Campos do endereço
    cep = forms.CharField(max_length=9, required=True)
    logradouro = forms.CharField(max_length=150, required=True)
    numero = forms.CharField(max_length=10, required=True)
    complemento = forms.CharField(max_length=50, required=False)
    bairro = forms.CharField(max_length=100, required=True)
    cidade = forms.CharField(max_length=100, required=True)
    estado = forms.ChoiceField(choices=Endereco.UF_CHOICES, required=True)

    # Override do cpf para aceirar a máscara
    cpf = forms.CharField(max_length=14, required=True)

    class Meta:
        model = Doador
        fields = ["nome", "cpf", "data_nasc", "sexo", "tipo_sang", "telefone", "email"]

    def clean(self):
        cleaned = super().clean()

        # limpar CPF
        cpf = cleaned.get("cpf")
        if cpf:
            cleaned["cpf"] = sub(r"\D", "", cpf)

        # limpar CEP
        cep = cleaned.get("cep")
        if cep:
            cleaned["cep"] = sub(r"\D", "", cep)

        return cleaned
