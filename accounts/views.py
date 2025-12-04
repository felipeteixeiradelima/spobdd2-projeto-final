from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from accounts.forms import *
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

def cadastro_colaborador(request):
    if request.method == "POST":
        form = ColaboradorCreateForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data["password"]
            )

            colaborador = form.save(commit=False)
            colaborador.user = user
            colaborador.email = email
            colaborador.save()

            messages.success(request, "Colaborador cadastrado com sucesso!")
            
            next_url = request.GET.get("next") or request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("colaboradores_list")

    else:
        form = ColaboradorCreateForm()

    return render(request, "accounts/cadastro_colaborador.html", {"form": form})

def escolher_perfil(request):
    user = request.user

    return render(request, "accounts/escolher_perfil.html", {
        "is_doador": hasattr(user, "doador_profile"),
        "is_colaborador": hasattr(user, "colaborador_profile"),
    })

@login_required
def minha_conta(request):
    user = request.user

    doador = getattr(user, "doador_profile", None)
    colaborador = getattr(user, "colaborador_profile", None)

    return render(request, "accounts/minha_conta.html", {
        "doador": doador,
        "colaborador": colaborador,
    })


@login_required
def minha_conta_editar_doador(request):
    doador = getattr(request.user, "doador_profile", None)
    if not doador:
        messages.error(request, "Você não é um doador.")
        return redirect("minha_conta")

    if request.method == "POST":
        form = EditarDoadorForm(request.POST, instance=doador)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect("minha_conta")
    else:
        form = EditarDoadorForm(instance=doador)

    return render(request, "accounts/editar_doador.html", {"form": form})


@login_required
def minha_conta_editar_endereco(request):
    doador = getattr(request.user, "doador_profile", None)
    if not doador or not doador.endereco:
        messages.error(request, "Você não possui endereço cadastrado.")
        return redirect("minha_conta")

    endereco = doador.endereco

    if request.method == "POST":
        form = EditarEnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            messages.success(request, "Endereço atualizado com sucesso!")
            return redirect("minha_conta")
    else:
        form = EditarEnderecoForm(instance=endereco)

    return render(request, "accounts/editar_endereco.html", {"form": form})


@login_required
def minha_conta_editar_colaborador(request):
    colaborador = getattr(request.user, "colaborador_profile", None)
    if not colaborador:
        messages.error(request, "Você não é um colaborador.")
        return redirect("minha_conta")

    if request.method == "POST":
        form = EditarColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas com sucesso!")
            return redirect("minha_conta")
    else:
        form = EditarColaboradorForm(instance=colaborador)

    return render(request, "accounts/editar_colaborador.html", {"form": form})


@login_required
def excluir_conta(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Sua conta foi excluída permanentemente.")
        return redirect("homepage")

    return render(request, "accounts/confirmar_exclusao_conta.html")
