from django.contrib import admin
from .models import Campanha, PontoColeta, Hospital, CampanhaColaborador, AmostraSangue, Doacao, Agendamento, PontoCampanha

admin.site.register(Campanha)
admin.site.register(PontoColeta)
admin.site.register(Hospital)
admin.site.register(CampanhaColaborador)
admin.site.register(AmostraSangue)
admin.site.register(Doacao)
admin.site.register(Agendamento)
admin.site.register(PontoCampanha)
