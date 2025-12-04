from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="homepage"), name="logout"),
    path("cadastro/", cadastro_doador, name="cadastro_doador"),
    path("cadastro-colaborador/", cadastro_colaborador, name="cadastro_colaborador"),
    path("escolher-perfil/", escolher_perfil, name="escolher_perfil"),
    path("minha-conta/", minha_conta, name="minha_conta"),
    path("minha-conta/editar-doador/", minha_conta_editar_doador, name="minha_conta_editar_doador"),
    path("minha-conta/editar-endereco/", minha_conta_editar_endereco, name="minha_conta_editar_endereco"),
    path("minha-conta/editar-colaborador/", minha_conta_editar_colaborador, name="minha_conta_editar_colaborador"),
    path("minha-conta/excluir/", excluir_conta, name="excluir_conta"),
]
