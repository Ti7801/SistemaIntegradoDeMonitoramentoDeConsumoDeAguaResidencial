from django.db import models
from django.urls import reverse


class Cliente(models.Model):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino')
    )
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30, null=False, blank=False)
    cpf = models.CharField(max_length=11, blank=False, unique=True, null=False)
    telefone = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(blank=False, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO, null=False)
    data_nascimento = models.DateField(blank=False, null=False)
    

    def get_absolute_url(self):
        return reverse('InterfaceWeb:listaClientes')
    
    def __str__(self):
        return f'{self.id_cliente}::{self.nome}::{self.cpf}::{self.telefone}::{self.email}::{self.sexo}::{self.data_nascimento}'
    

class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=20, blank=False, null=False)
    bairro = models.CharField(max_length=20, blank=False, null=False)
    rua = models.CharField(max_length=40, blank=False, null=False)
    numero = models.CharField(max_length=10, blank=False, null=False)
    complemento = models.CharField(max_length=100, blank=False, null=False)
    cep = models.CharField(max_length=20, blank=False, null=False)
    consumo_total = models.IntegerField(max_length=100, null=False, blank=False, default=0)
    consumo_ultimo_mes = models.IntegerField(max_length=100, null=False, default=0, blank=False)
    consumo_inicio_mes = models.IntegerField(max_length=100, null=False, default=0, blank=False)

    def get_absolute_url(self):
        return reverse('InterfaceWeb:listaClientes')
    
    def __str__(self):
        return f'{self.id_endereco}::{self.cliente}::{self.cidade}::{self.bairro}::{self.rua}::{self.numero}::{self.complemento}::{self.cep}::{self.consumo_total}::{self.consumo_ultimo_mes}::{self.consumo_inicio_mes}'



class Fatura(models.Model):
    pagamento = (
        (True, 'Sim'),
        (False, 'Nao')
    )
    id_fatura = models.AutoField(primary_key=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name="enderecos")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="clientes")
    consumo_mensal = models.CharField(max_length=100, null=False, blank=False)
    mes = models.CharField(max_length=20, null=False, blank=False)
    ano = models.CharField(max_length=10, null=False, blank=False)
    valor_pagar = models.CharField(max_length=20, null=False, blank=False)
    fatura_paga = models.CharField(max_length=5, choices = pagamento, null=False)
    fatura_nome = models.CharField(max_length=20, null=False, blank=False)

    def get_absolute_url(self):
        return reverse('InterfaceWeb:inicio')
    
    def __str__(self):
        return f'{self.id_fatura}::{self.endereco}::{self.cliente}::{self.consumo_mensal}::{self.mes}::{self.ano}::{self.valor_pagar}::{self.fatura_paga}::{self.fatura_nome}'
    

class InterfaceWebUser(models.Model):
    id_adm = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, blank=False, null=False, unique=True)
    nome = models.CharField(max_length=40, null=False, blank=False)
    login = models.CharField(max_length=50, null=False, blank=False)
    senha = models.CharField(max_length=50, null=False, blank=False)

    def get_absolute_url(self):
        return reverse('InterfaceWeb:login')
    
    def __str__(self):
        return f'{self.id_adm}::{self.cpf}::{self.nome}::{self.login}::{self.senha}'


