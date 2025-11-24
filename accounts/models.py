from django.db import models
from django.contrib.auth.models import User


class Endereco(models.Model):
    UF_CHOICES = [
        ("AC", "AC"),
        ("AL", "AL"),
        ("AP", "AP"),
        ("AM", "AM"),
        ("BA", "BA"),
        ("CE", "CE"),
        ("DF", "DF"),
        ("ES", "ES"),
        ("GO", "GO"),
        ("MA", "MA"),
        ("MT", "MT"),
        ("MS", "MS"),
        ("MG", "MG"),
        ("PA", "PA"),
        ("PB", "PB"),
        ("PR", "PR"),
        ("PE", "PE"),
        ("PI", "PI"),
        ("RJ", "RJ"),
        ("RN", "RN"),
        ("RS", "RS"),
        ("RO", "RO"),
        ("RR", "RR"),
        ("SC", "SC"),
        ("SP", "SP"),
        ("SE", "SE"),
        ("TO", "TO"),
    ]

    id_endereco = models.BigAutoField(primary_key=True)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=UF_CHOICES)

    def __str__(self):
        return f"{self.logradouro}, {self.numero or ''} - {self.cidade}/{self.estado}"


class Doador(models.Model):
    TIPO_SANGUINEO_CHOICES = [
        ('NA', 'Não sei'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    id_doador = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doador_profile', null=True, blank=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    data_nasc = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    tipo_sang = models.CharField(max_length=3, choices=TIPO_SANGUINEO_CHOICES)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.tipo_sang})"


class Colaborador(models.Model):
    id_colaborador = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='colaborador_profile', null=True, blank=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    data_nasc = models.DateField()
    cargo = models.CharField(max_length=50, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nome} - {self.cargo or 'Colaborador'}"
