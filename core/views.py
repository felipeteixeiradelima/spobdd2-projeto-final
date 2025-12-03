from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import AgendamentoForm, EditarCampanhaForm, PontoColetaCreateForm, EditarPontoForm, CampanhaCreateForm, AmostraForm, DoacaoForm
from accounts.models import Doador, Colaborador, Endereco
from django.http import JsonResponse
from core.models import PontoColeta, PontoCampanha, Agendamento, Campanha, CampanhaColaborador, AmostraSangue
from datetime import timedelta, date
from core.models import Doacao

def colaborador_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, "colaborador_profile"):
            messages.error(request, "Acesso permitido apenas para colaboradores.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

def homepage(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/sobre.html")

@login_required
def agendamento_view(request):
    print("POST:", request.POST)

    doador = request.user.doador_profile

    if request.method == "POST":
        form = AgendamentoForm(request.POST, doador=doador)

        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.doador = doador
            agendamento.save()
            messages.success(request, "Agendamento realizado com sucesso!")
            return redirect("meus_agendamentos")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = AgendamentoForm(doador=doador)

    return render(request, "core/agendamento.html", {"form": form})

@login_required
def meus_agendamentos(request):
    doador = Doador.objects.get(user=request.user)
    agendamentos = Agendamento.objects.filter(doador_id=doador).order_by("-data_agendada")
    return render(request, "core/meus_agendamentos.html", {"agendamentos": agendamentos})

@login_required
def cancelar_agendamento(request, agendamento_id):
    doador = Doador.objects.get(user=request.user)
    agendamento = Agendamento.objects.get(id_agendamento=agendamento_id, doador_id=doador)

    agendamento.status = "cancelado"
    agendamento.save()

    messages.success(request, "Agendamento cancelado com sucesso!")
    return redirect("meus_agendamentos")

@login_required
def get_pontos_por_campanha(request, id_campanha):
    try:
        pontos_ids = PontoCampanha.objects.filter(campanha_id=id_campanha)\
                                        .values_list("ponto_id", flat=True)

        pontos = PontoColeta.objects.filter(id_ponto__in=pontos_ids)

        dados = [{"id_ponto": p.id_ponto, "nome": p.nome} for p in pontos]

        return JsonResponse({"pontos": dados})
    except Exception as e:
        return JsonResponse({"pontos": []})

@login_required
def campanhas_list(request):

    usuario = request.user

    # Determinar tipo de usuário
    is_doador = Doador.objects.filter(user=usuario).exists()
    is_colaborador = Colaborador.objects.filter(user=usuario).exists()

    # Ver todas as campanhas
    if is_doador or is_colaborador:
        campanhas = Campanha.objects.all().order_by("-data_inicio")

    # fallback (não deveria acontecer)
    else:
        campanhas = Campanha.objects.none()

    # Filtro GET opcional: ?status=ativa
    status = request.GET.get("status")
    if status:
        campanhas = campanhas.filter(status=status)

    return render(request, "core/campanhas_list.html", {
        "campanhas": campanhas,
        "is_doador": is_doador,
        "is_colaborador": is_colaborador,
        "status": status or "",
    })

@login_required
def campanha_detail(request, id_campanha):
    campanha = get_object_or_404(Campanha, id_campanha=id_campanha)

    pontos_campanha = PontoCampanha.objects.filter(campanha_id=id_campanha)

    pontos_id = [pc.ponto.id_ponto for pc in pontos_campanha]

    pontos = PontoColeta.objects.filter(id_ponto__in=pontos_id)

    context = {
        "campanha": campanha,
        "pontos": pontos
    }

    return render(request, "core/campanha_detail.html", context)

@login_required
def ponto_detail(request, ponto_id):
    ponto = get_object_or_404(PontoColeta, id_ponto=ponto_id)
    return render(request, "core/ponto_detail.html", {
        "ponto": ponto,
    })

@login_required
def campanhas_json(request):
    campanhas = Campanha.objects.all().order_by("-data_inicio")

    data = []
    for c in campanhas:
        data.append({
            "id": c.id_campanha,
            "nome": c.nome,
            "data_inicio": c.data_inicio.strftime("%d/%m/%Y"), # type: ignore
            "data_fim": c.data_fim.strftime("%d/%m/%Y"), # type: ignore
            "status": c.get_status_display(), # type: ignore
        })

    return JsonResponse({"data": data})

@login_required
@colaborador_required
def cadastrar_ponto(request):
    if request.method == "POST":
        form = PontoColetaCreateForm(request.POST)

        if form.is_valid():
            # Criar endereço
            endereco = Endereco.objects.create(
                cep=form.cleaned_data["cep"],
                logradouro=form.cleaned_data["logradouro"],
                numero=form.cleaned_data["numero"],
                complemento=form.cleaned_data["complemento"],
                bairro=form.cleaned_data["bairro"],
                cidade=form.cleaned_data["cidade"],
                estado=form.cleaned_data["estado"],
            )

            # Criar ponto de coleta
            ponto = form.save(commit=False)
            ponto.endereco = endereco
            ponto.save()

            messages.success(request, "Ponto de coleta cadastrado com sucesso!")

            next_url = request.session.pop("return_to_campanha", None)
            if next_url:
                return redirect("cadastrar_campanha")

            return redirect("pontos_list")  # ou outra página da sua escolha

    else:
        form = PontoColetaCreateForm()

    return render(request, "core/cadastrar_ponto.html", {"form": form})

@login_required
@colaborador_required
def editar_campanha(request, id_campanha):
    campanha = get_object_or_404(Campanha, id_campanha=id_campanha)

    if request.method == "POST":
        form = EditarCampanhaForm(request.POST, instance=campanha)
        if form.is_valid():
            form.save()
            messages.success(request, "Campanha atualizada com sucesso!")
            return redirect("campanha_detail", id_campanha=id_campanha)
    else:
        form = EditarCampanhaForm(instance=campanha)

    return render(request, "core/editar_campanha.html", {"form": form, "campanha": campanha})

@login_required
@colaborador_required
def editar_ponto(request, id_ponto):
    ponto = get_object_or_404(PontoColeta, id_ponto=id_ponto)
    endereco = ponto.endereco

    if request.method == "POST":
        form = EditarPontoForm(request.POST, ponto=ponto, instance=ponto)
        if form.is_valid():

            if endereco:
                # Atualizar endereço
                endereco.cep = form.cleaned_data["cep"] 
                endereco.logradouro = form.cleaned_data["logradouro"]
                endereco.numero = form.cleaned_data["numero"]
                endereco.complemento = form.cleaned_data["complemento"]
                endereco.bairro = form.cleaned_data["bairro"]
                endereco.cidade = form.cleaned_data["cidade"]
                endereco.estado = form.cleaned_data["estado"]
                endereco.save()

            # Atualizar ponto
            form.save()

            messages.success(request, "Ponto atualizado com sucesso!")
            return redirect("ponto_detail", id_ponto=id_ponto)
    else:
        form = EditarPontoForm(ponto=ponto, instance=ponto)

    return render(request, "core/editar_ponto.html", {"form": form, "ponto": ponto})

@login_required
@colaborador_required
def cadastrar_campanha(request):
    # Caso tenha sido redirecionado do cadastro de colaborador/ponto
    # mantemos os valores anteriores
    initial_data = request.session.pop("campanha_form_data", None)

    if request.method == "POST":
        form = CampanhaCreateForm(request.POST)

        if "add_colaborador" in request.POST:
            # salva dados do form temporariamente
            request.session["campanha_form_data"] = request.POST
            return redirect("cadastrar_colaborador")

        if "add_ponto" in request.POST:
            request.session["campanha_form_data"] = request.POST
            return redirect("cadastrar_ponto")

        if form.is_valid():
            campanha = form.save()

            # salvar relacionamentos nos modelos associativos
            for colaborador in form.cleaned_data["colaboradores"]:
                CampanhaColaborador.objects.create(
                    campanha=campanha,
                    colaborador=colaborador
                )

            for ponto in form.cleaned_data["pontos"]:
                PontoCampanha.objects.create(
                    campanha=campanha,
                    ponto=ponto
                )

            messages.success(request, "Campanha cadastrada com sucesso!")
            return redirect("campanha_detail", id_campanha=campanha.id_campanha)

    else:
        if initial_data:
            form = CampanhaCreateForm(initial_data)
        else:
            form = CampanhaCreateForm()

    return render(request, "core/cadastrar_campanha.html", {"form": form})

@colaborador_required
@login_required
def pontos_list(request):
    pontos = PontoColeta.objects.select_related("endereco").order_by("nome")

    return render(request, "core/pontos_list.html", {
        "pontos": pontos
    })

@login_required
@colaborador_required
def campanha_delete(request, id_campanha):
    campanha = get_object_or_404(Campanha, id_campanha=id_campanha)

    if request.method == "POST":
        campanha.delete()
        messages.success(request, "Campanha excluída com sucesso!")
        return redirect("campanhas_list")

    return render(request, "core/confirm_delete.html", {
        "obj": campanha,
        "type": "campanha",
        "back_url": "campanha_detail",
        "id": id_campanha,
    })

@login_required
@colaborador_required
def ponto_delete(request, ponto_id):
    ponto = get_object_or_404(PontoColeta, id_ponto=ponto_id)

    if request.method == "POST":
        ponto.delete()
        messages.success(request, "Ponto de coleta excluído com sucesso!")
        return redirect("pontos_list")

    return render(request, "core/confirm_delete.html", {
        "obj": ponto,
        "type": "ponto",
        "back_url": "ponto_detail",
        "id": ponto_id,
    })

@login_required
@colaborador_required
def amostras_list(request):
    amostras = AmostraSangue.objects.all()
    return render(request, "core/amostras_list.html", {"amostras": amostras})

@login_required
@colaborador_required
def amostra_create(request):
    if request.method == "POST":
        form = AmostraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Amostra cadastrada com sucesso!")
            return redirect("amostras_list")
    else:
        form = AmostraForm()
    return render(request, "core/amostra_form.html", {"form": form, "titulo": "Cadastrar Amostra"})

@login_required
@colaborador_required
def amostra_edit(request, id_amostra):
    amostra = get_object_or_404(AmostraSangue, id_amostra=id_amostra)

    if request.method == "POST":
        form = AmostraForm(request.POST, instance=amostra)
        if form.is_valid():
            form.save()
            messages.success(request, "Amostra atualizada com sucesso!")
            return redirect("amostra_detail", id_amostra=id_amostra)
    else:
        form = AmostraForm(instance=amostra)

    return render(request, "core/amostra_form.html", {"form": form, "titulo": "Editar Amostra"})

@login_required
@colaborador_required
def amostra_detail(request, id_amostra):
    amostra = get_object_or_404(AmostraSangue, id_amostra=id_amostra)
    return render(request, "core/amostra_detail.html", {"amostra": amostra})

@login_required
@colaborador_required
def amostra_delete(request, id_amostra):
    amostra = get_object_or_404(AmostraSangue, id_amostra=id_amostra)

    if request.method == "POST":
        amostra.delete()
        messages.success(request, "Amostra de Sangue excluída com sucesso!")
        return redirect("amostra_list")

    return render(request, "core/confirm_delete.html", {
        "obj": amostra,
        "type": "amostra",
        "back_url": "amostra_detail",
        "id": id_amostra,
    })

@login_required
@colaborador_required
def doacoes_list(request):
    doacoes = Doacao.objects.select_related("doador", "ponto", "amostra", "campanha")
    return render(request, "core/doacoes_list.html", {"doacoes": doacoes})

@login_required
@colaborador_required
def doacao_create(request):
    if request.method == "POST":
        form_doacao = DoacaoForm(request.POST)
        form_amostra = AmostraForm(request.POST)

        if form_doacao.is_valid():

            # criar amostra se marcado
            if form_doacao.cleaned_data.get("criar_amostra") and form_amostra.is_valid():
                amostra = form_amostra.save()
            else:
                amostra = None

            doacao = form_doacao.save(commit=False)
            doacao.amostra = amostra
            doacao.save()

            messages.success(request, "Doação cadastrada com sucesso!")
            return redirect("doacoes_list")

    else:
        form_doacao = DoacaoForm()
        form_amostra = AmostraForm()

    return render(request, "core/doacao_form.html", {
        "form_doacao": form_doacao,
        "form_amostra": form_amostra
    })

@login_required
@colaborador_required
def doacao_edit(request, id_doacao):
    doacao = get_object_or_404(Doacao, id_doacao=id_doacao)

    if request.method == "POST":
        form = DoacaoForm(request.POST, instance=doacao)
        if form.is_valid():
            form.save()
            messages.success(request, "Doação atualizada!")
            return redirect("doacao_detail", id_doacao=id_doacao)
    else:
        form = DoacaoForm(instance=doacao)

    return render(request, "core/doacao_form_edit.html", {"form_doacao": form})

@login_required
@colaborador_required
def doacao_detail(request, id_doacao):
    doacao = get_object_or_404(Doacao, id_doacao=id_doacao)
    return render(request, "core/doacao_detail.html", {"doacao": doacao})

@login_required
@colaborador_required
def doacao_delete(request, id_doacao):
    doacao = get_object_or_404(Doacao, id_doacao=id_doacao)

    if request.method == "POST":
        doacao.delete()
        messages.success(request, "Doação excluída com sucesso!")
        return redirect("doacao_list")

    return render(request, "core/confirm_delete.html", {
        "obj": doacao,
        "type": "doacao",
        "back_url": "doacao_detail",
        "id": id_doacao,
    })

@login_required
@colaborador_required
def area_colaborador(request):
    return render(request, "core/area_colaborador.html")
