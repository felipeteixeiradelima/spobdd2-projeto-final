from re import sub

from django import forms
from django.utils.timezone import now
from datetime import timedelta
from accounts.models import Colaborador, Endereco
from core.models import Agendamento, Campanha, PontoColeta, Doacao, PontoCampanha, AmostraSangue


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ["campanha", "ponto", "data_agendada"]
        widgets = {
            "data_agendada": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        self.doador = kwargs.pop("doador")
        super().__init__(*args, **kwargs)

        # Apenas campanhas válidas
        self.fields["campanha"].queryset = Campanha.objects.exclude( # type: ignore
            status__in=["finalizada", "cancelada"]
        )

        # O campo ponto começa vazio
        self.fields["ponto"].queryset = PontoColeta.objects.none() # type: ignore

        # pega o ID da campanha vinda do POST, initial ou instance
        campanha_id = (
            self.data.get("campanha")
            or self.initial.get("campanha")
            or (self.instance.campanha_id if self.instance.pk else None)
        )

        if campanha_id:
            try:
                campanha = Campanha.objects.get(id_campanha=campanha_id)

                # pontos associados via tabela intermediária
                self.fields["ponto"].queryset = PontoColeta.objects.filter( # type: ignore
                    pontocampanha__campanha=campanha
                ).distinct()

            except Campanha.DoesNotExist:
                pass

    def clean(self):
        cleaned = super().clean()

        campanha = cleaned.get("campanha")
        ponto = cleaned.get("ponto")
        data_agendada = cleaned.get("data_agendada")

        print(ponto)

        print("ERROS", self.errors)

        if not campanha or not ponto or not data_agendada:
            return cleaned

        # Campanha encerrada
        if campanha.status in ["finalizada", "cancelada"]:
            raise forms.ValidationError("Não é possível agendar em campanhas encerradas.")

        # Data fora do período
        if data_agendada < campanha.data_inicio or data_agendada > campanha.data_fim:
            raise forms.ValidationError(
                f"A data deve estar entre {campanha.data_inicio} e {campanha.data_fim}."
            )

        # Doador já tem agendamento nesta campanha
        if Agendamento.objects.filter(
            doador=self.doador,
            campanha=campanha
        ).exists():
            raise forms.ValidationError("Você já possui um agendamento nesta campanha.")

        # Doador doou nos últimos 60 dias
        limite = now().date() - timedelta(days=60)

        if Doacao.objects.filter(
            doador=self.doador,
            data_doacao__gte=limite
        ).exists():
            raise forms.ValidationError(
                "Você só pode agendar novamente após 60 dias da última doação."
            )

        # O ponto precisa pertencer à campanha
        if not PontoCampanha.objects.filter(ponto=ponto, campanha=campanha):
            raise forms.ValidationError("Este ponto não pertence à campanha selecionada.")

        return cleaned

class PontoColetaCreateForm(forms.ModelForm):
    # Campos do endereço (embutidos)
    cep = forms.CharField(max_length=9, required=True)
    logradouro = forms.CharField(max_length=150, required=True)
    numero = forms.CharField(max_length=10, required=True)
    complemento = forms.CharField(max_length=50, required=False)
    bairro = forms.CharField(max_length=100, required=True)
    cidade = forms.CharField(max_length=100, required=True)
    estado = forms.ChoiceField(choices=Endereco.UF_CHOICES, required=True)

    class Meta:
        model = PontoColeta
        fields = ["nome"]

    def clean_cep(self):
        cep = self.cleaned_data["cep"]
        return sub(r"\D", "", cep)

class CampanhaCreateForm(forms.ModelForm):
    colaboradores = forms.ModelMultipleChoiceField(
        queryset=Colaborador.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    pontos = forms.ModelMultipleChoiceField(
        queryset=PontoColeta.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )

    class Meta:
        model = Campanha
        fields = [
            "nome",
            "descricao",
            "data_inicio",
            "data_fim",
            "publico_alvo",
            "status",
            "colaboradores",
            "pontos",
        ]
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim": forms.DateInput(attrs={"type": "date"}),
        }

class EditarCampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ["nome", "descricao", "data_inicio", "data_fim", "status", "publico_alvo"]
        widgets = {
            # define explicitamente o formato ISO que <input type="date"> exige
            "data_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "data_fim": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se o form foi instanciado com uma instance (editar), força initial no formato ISO
        if self.instance and getattr(self.instance, "data_inicio", None):
            self.fields["data_inicio"].initial = self.instance.data_inicio.strftime("%Y-%m-%d")
        if self.instance and getattr(self.instance, "data_fim", None):
            self.fields["data_fim"].initial = self.instance.data_fim.strftime("%Y-%m-%d")

class EditarPontoForm(forms.ModelForm):
    # campos do endereço
    cep = forms.CharField()
    logradouro = forms.CharField()
    numero = forms.CharField()
    complemento = forms.CharField(required=False)
    bairro = forms.CharField()
    cidade = forms.CharField()
    estado = forms.ChoiceField(choices=Endereco.UF_CHOICES)

    class Meta:
        model = PontoColeta
        fields = ["nome"]

    def __init__(self, *args, **kwargs):
        ponto = kwargs.pop("ponto")
        super().__init__(*args, **kwargs)

        endereco = ponto.endereco
        self.fields["cep"].initial = endereco.cep
        self.fields["logradouro"].initial = endereco.logradouro
        self.fields["numero"].initial = endereco.numero
        self.fields["complemento"].initial = endereco.complemento
        self.fields["bairro"].initial = endereco.bairro
        self.fields["cidade"].initial = endereco.cidade
        self.fields["estado"].initial = endereco.estado

class AmostraForm(forms.ModelForm):
    class Meta:
        model = AmostraSangue
        fields = ["tipo_sang", "quantidade_ml", "validade", "status"]
        widgets = {
            "validade": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se o form foi instanciado com uma instance (editar), força initial no formato ISO
        if self.instance and getattr(self.instance, "validade", None):
            self.fields["validade"].initial = self.instance.validade.strftime("%Y-%m-%d")

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['doador', 'campanha', 'ponto', 'data_doacao']
        widgets = {
            'data_doacao': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se o form foi instanciado com uma instance (editar), força initial no formato ISO
        if self.instance and getattr(self.instance, "data_doacao", None):
            self.fields["data_doacao"].initial = self.instance.data_doacao.strftime("%Y-%m-%d")

class EditarColaboradorForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirmarSenha = forms.CharField(widget=forms.PasswordInput(), required=True)

    cpf = forms.CharField(max_length=14, required=True)

    class Meta:
        model = Colaborador
        fields = ["nome", "cpf", "data_nasc", "telefone", "cargo"]
        widgets = {
            "data_nasc": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se o form foi instanciado com uma instance (editar), força initial no formato ISO
        if self.instance and getattr(self.instance, "email", None):
            self.fields["email"].initial = self.instance.email
        if self.instance and getattr(self.instance, "data_fim", None):
            self.fields["data_nasc"].initial = self.instance.data_nasc.strftime("%Y-%m-%d")
