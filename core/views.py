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
    # Obtém o doador vinculado ao usuário logado
    try:
        doador = Doador.objects.get(user=request.user)
    except Doador.DoesNotExist:
        messages.error(request, "Apenas doadores podem realizar agendamentos.")
        return redirect("homepage")

    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            # Valida se doador já tem um agendamento para essa campanha
            if Agendamento.objects.filter(id_doador=doador, id_campanha=form.cleaned_data["id_campanha"]).exists():
                messages.error(request, "Você já possui um agendamento nesta campanha.")
                return redirect("agendamento")

            # Valida se doador doou nos últimos 90 dias
            ultima_doacao = Doacao.objects.filter(id_doador=doador).order_by("-data_doacao").first()
            if ultima_doacao:
                proxima_data = ultima_doacao.data_doacao + timedelta(days=90)
                if date.today() < proxima_data:
                    messages.error(request, f"Você só poderá agendar doação após {proxima_data.strftime('%d/%m/%Y')}.")
                    return redirect("agendamento")

            agendamento = form.save(commit=False)
            agendamento.id_doador = doador
            agendamento.save()
            messages.success(request, "Agendamento realizado com sucesso!")
            return redirect("homepage")
    else:
        form = AgendamentoForm()

    return render(request, "core/agendamento.html", {"form": form})

@login_required
def meus_agendamentos(request):
    doador = Doador.objects.get(user=request.user)
    agendamentos = Agendamento.objects.filter(id_doador=doador).order_by("-data_agendada")
    return render(request, "core/meus_agendamentos.html", {"agendamentos": agendamentos})

@login_required
def cancelar_agendamento(request, agendamento_id):
    doador = Doador.objects.get(user=request.user)
    agendamento = Agendamento.objects.get(id=agendamento_id, id_doador=doador)

    agendamento.status = "cancelado"
    agendamento.save()

    messages.success(request, "Agendamento cancelado.")
    return redirect("meus_agendamentos")

@login_required
def get_pontos_por_campanha(request, campanha_id):
    pontos_ids = PontoCampanha.objects.filter(id_campanha_id=campanha_id)\
                                      .values_list("id_ponto_id", flat=True)

    pontos = PontoColeta.objects.filter(id__in=pontos_ids)

    dados = [
        {"id": p.id, "nome": p.nome} # type: ignore
        for p in pontos
    ]

    return JsonResponse({"pontos": dados})

@login_required
def campanhas_list(request):

    usuario = request.user

    # Determinar tipo de usuário
    is_doador = Doador.objects.filter(user=usuario).exists()
    is_colaborador = Colaborador.objects.filter(user=usuario).exists()

    # Doador vê apenas campanhas ATIVAS
    if is_doador:
        campanhas = Campanha.objects.filter(status="ativa").order_by("data_inicio")

    # Colaborador vê todas
    elif is_colaborador:
        campanhas = Campanha.objects.all().order_by("data_inicio")

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
def campanha_detail(request, campanha_id):
    campanha = get_object_or_404(Campanha, id=campanha_id)
    return render(request, "core/campanha_detail.html", {"campanha": campanha})
