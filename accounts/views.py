from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from accounts.forms import DoadorCreateForm
from accounts.models import Endereco

class CustomAuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Email e/ou senha inválidos!"
        ),
    }

class CustomLoginView(LoginView):
    authentication_form = CustomAuthForm
    template_name = "accounts/login.html"

def cadastro_doador(request):
    if request.method == "POST":
        form = DoadorCreateForm(request.POST)

        if form.is_valid():

            # Criar User
            email = form.cleaned_data["email"]
            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data["password"],
            )

            # Criar Endereco
            endereco = Endereco.objects.create(
                cep=form.cleaned_data["cep"],
                logradouro=form.cleaned_data["logradouro"],
                numero=form.cleaned_data["numero"],
                complemento=form.cleaned_data["complemento"],
                bairro=form.cleaned_data["bairro"],
                cidade=form.cleaned_data["cidade"],
                estado=form.cleaned_data["estado"],
            )

            # Criar Doador
            doador = form.save(commit=False)
            doador.user = user
            doador.endereco = endereco
            doador.save()

            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("login")

    else:
        form = DoadorCreateForm()

    return render(request, "accounts/cadastro.html", {"form": form})
