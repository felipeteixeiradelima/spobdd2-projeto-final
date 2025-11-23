from django.urls import path
from .views import CustomLoginView, cadastro_doador
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="homepage"), name="logout"),
    path("cadastro/", cadastro_doador, name="cadastro_doador"),
]
