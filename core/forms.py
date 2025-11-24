from django import forms
from django.utils.timezone import now
from datetime import timedelta
from core.models import Agendamento, Campanha, PontoColeta, Doacao, PontoCampanha


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
