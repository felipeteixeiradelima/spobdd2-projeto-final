from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import AgendamentoForm
from accounts.models import Doador, Colaborador
from django.http import JsonResponse
from core.models import PontoColeta, PontoCampanha, Agendamento, Campanha
from datetime import timedelta, date
from core.models import Doacao

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

    return JsonResponse({"campanhas": data})
