from django import forms
from core.models import Agendamento, Campanha, PontoColeta
from datetime import date

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ["data_agendada", "campanha", "ponto"]
        widgets = {
            "data_agendada": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apenas campanhas ativas
        self.fields["campanha"].queryset = Campanha.objects.filter(status="ativa") # type: ignore

    def clean_data_agendada(self):
        data = self.cleaned_data["data_agendada"]
        if data < date.today():
            raise forms.ValidationError("Insira uma data válida.")
        return data
