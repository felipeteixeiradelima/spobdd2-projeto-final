from django.db import models
from accounts.models import Endereco, Doador, Colaborador


class AmostraSangue(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('utilizada', 'Utilizada'),
        ('expirada', 'Expirada'),
        ('reservada', 'Reservada'),
    ]

    id_amostra = models.BigAutoField(primary_key=True)
    tipo_sang = models.CharField(max_length=3)
    quantidade_ml = models.PositiveIntegerField()
    validade = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')

    def __str__(self):
        return f"{self.tipo_sang} ({self.status})"


class PontoColeta(models.Model):
    id_ponto = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class Hospital(models.Model):
    id_hospital = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class Campanha(models.Model):
    STATUS_CHOICES = [
        ('planejada', 'Planejada'),
        ('ativa', 'Ativa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    id_campanha = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    publico_alvo = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejada')

    def __str__(self):
        return f"{self.nome} ({self.status})"


class CampanhaColaborador(models.Model):
    id_campanha_colaborador = models.BigAutoField(primary_key=True)
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    funcao = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'campanha_colaborador'  # nome claro e consistente com o banco
        unique_together = ('campanha', 'colaborador')  # impede duplicidade
        verbose_name = 'Colaborador da Campanha'
        verbose_name_plural = 'Colaboradores de Campanhas'

    def __str__(self):
        return f"{self.colaborador.nome} em {self.campanha.nome}"


class PontoCampanha(models.Model):
    ponto = models.ForeignKey(PontoColeta, on_delete=models.CASCADE)
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ponto', 'campanha')

    def __str__(self):
        return f"{self.campanha.nome} em {self.ponto.nome}"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
        ('expirado', 'Expirado'),
    ]

    id_agendamento = models.BigAutoField(primary_key=True)
    data_agendada = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado')
    doador = models.ForeignKey(Doador, on_delete=models.CASCADE)
    campanha = models.ForeignKey(Campanha, on_delete=models.SET_NULL, null=True, blank=True)
    ponto = models.ForeignKey(PontoColeta, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Agendamento de {self.doador.nome} em {self.data_agendada}"


class Doacao(models.Model):
    id_doacao = models.BigAutoField(primary_key=True)
    data_doacao = models.DateField()
    doador = models.ForeignKey(Doador, on_delete=models.CASCADE)
    amostra = models.ForeignKey(AmostraSangue, on_delete=models.SET_NULL, null=True, blank=True)
    ponto = models.ForeignKey(PontoColeta, on_delete=models.SET_NULL, null=True, blank=True)
    campanha = models.ForeignKey(Campanha, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Doação #{self.id_doacao} - {self.doador.nome}"
