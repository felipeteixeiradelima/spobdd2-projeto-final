from django.urls import path
from .views import homepage, agendamento_view, get_pontos_por_campanha, meus_agendamentos, cancelar_agendamento, campanhas_list, campanha_detail, about, ponto_detail


urlpatterns = [
    path("", homepage, name="homepage"),
    path("sobre/", about, name="sobre"),
    path("agendamento/", agendamento_view, name="agendamento"),
    path("meus-agendamentos/", meus_agendamentos, name="meus_agendamentos"),
    path("cancelar-agendamento/<int:agendamento_id>/", cancelar_agendamento, name="cancelar_agendamento"),
    path("ajax/pontos/<int:id_campanha>/", get_pontos_por_campanha, name="get_pontos_por_campanha"),
    path("campanhas/", campanhas_list, name="campanhas_list"),
    path("campanhas/<int:id_campanha>/", campanha_detail, name="campanha_detail"),
    path("ponto/<int:ponto_id>/", ponto_detail, name="ponto_detail"),
]
