from django.urls import path
from .views import CustomLoginView, cadastro_doador, cadastro_colaborador, escolher_perfil
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="homepage"), name="logout"),
    path("cadastro/", cadastro_doador, name="cadastro_doador"),
    path("cadastro-colaborador/", cadastro_colaborador, name="cadastro_colaborador"),
    path("escolher-perfil/", escolher_perfil, name="escolher_perfil"),
]
