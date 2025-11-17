from django.urls import path
from .views import CustomLoginView, cadastro_doador

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("cadastro/", cadastro_doador, name="cadastro_doador"),
]
