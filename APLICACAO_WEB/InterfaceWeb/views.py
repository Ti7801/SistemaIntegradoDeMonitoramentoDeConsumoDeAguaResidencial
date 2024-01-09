from InterfaceWeb.models  import Cliente, Endereco, Fatura, InterfaceWebUser
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from InterfaceWeb.forms import ClienteForm, EnderecoForm,cep_numeroForm, loginForm, cadastrarForm
from django.http import HttpResponseRedirect
from django.urls import is_valid_path, reverse_lazy
from django.shortcuts import render, redirect
from InterfaceWeb.funcoes import Salvar_no_Firebase, AEntidadeExiste, descompactar_string, descompactar_id, get_confirm_delete, consulta_firebase_consumo, CreateEnderecoFromQuerySet, CreateClientFromQuerySet, Valor_a_Pagar, salvar_novo_CPF_banco_dados
from datetime import datetime, date
from calendar import monthrange
from time import sleep
import threading


#Criar cliente
class ClienteCreate(CreateView):
    template_name = "templates/Admin/formulario_cliente.html"
    model = Cliente
    fields = ['nome', 'cpf', 'telefone', 'email', 'sexo', 'data_nascimento']
    sucess_url: reverse_lazy('InterfaceWeb:inicio')

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

#Listar cliente
class ClienteList(ListView):
    template_name = "templates/Admin/lista_clientes.html"
    model = Cliente

    def get_queryset(self):
        txt_nome = self.request.GET.get('nome')
        if txt_nome:
            cliente = Cliente.objects.filter(nome__icontains=txt_nome)
        else:
            cliente = Cliente.objects.all()          
        return cliente

#Editar cliente
class ClienteUpdate(UpdateView):
    template_name = "templates/Admin/formulario_cliente.html"
    model = Cliente
    fields = ['nome', 'cpf', 'telefone', 'email', 'sexo', 'data_nascimento']
    success_url: reverse_lazy('InterfaceWeb:inicio')

#Deletar cliente
class ClienteDelete(DeleteView):
    template_name = "templates/Admin/comfirm_deletar_cliente.html"
    model = Cliente
    fields = ['nome', 'cpf', 'telefone', 'email', 'sexo','data_nascimento']
    queryset = Cliente.objects.all()
    success_url = reverse_lazy('InterfaceWeb:listaClientes')

#Criar endereço
def CriarEndereco(request):
    if request.method == "GET":
        form = EnderecoForm()
        context = {
            'form':form
        }
        return render(request, "templates/Admin/criar_endereco.html", context)
    
    elif request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            text_cpf = form['cpf'].data
            clienteDados= Cliente.objects.all().filter(cpf=text_cpf)
            if(AEntidadeExiste(clienteDados)):
                endereco = Endereco()
                endereco.cidade = form['cidade'].data
                endereco.bairro = form['bairro'].data
                endereco.rua = form['rua'].data
                endereco.numero = form['numero'].data
                endereco.complemento = form['complemento'].data
                endereco.cep = form['cep'].data
                endereco.cliente = CreateClientFromQuerySet(clienteDados)
                endereco.cliente_id = descompactar_string(clienteDados,"id_cliente")

                Salvar_no_Firebase(endereco.numero, endereco.cep)
                endereco.save()

                return HttpResponseRedirect("/ListarClientes")
            
            else:
                msg = 'Cliente não encontrado. Verifique o CPF digitado!'

                context = {
                    'msg': msg
                }

                return render(request, "templates/Admin/mensagem_error.html", context)
            
        return render(request, "templates/Admin/mensagem_error.html")


#Editar endereço
def editarEndereco(request):
    
    form = cep_numeroForm(request.POST)
    text_cep = form['cep'].data
    text_num = form['numero'].data
    cep_numeroDados = Endereco.objects.all().filter(cep=text_cep).filter(numero=text_num)

    if len(cep_numeroDados) == 1:

        id = descompactar_string(cep_numeroDados, "cliente_id")
        cliente = Cliente.objects.all().filter(id_cliente=id)
        cpf = descompactar_string(cliente, "cpf")
        cidade = descompactar_string(cep_numeroDados, "cidade")
        bairro = descompactar_string(cep_numeroDados, "bairro")
        rua = descompactar_string(cep_numeroDados, "rua")
        numero = descompactar_string(cep_numeroDados, "numero")
        complemento = descompactar_string(cep_numeroDados, "complemento")
        cep = descompactar_string(cep_numeroDados, "cep")

        formEndereco = EnderecoForm()
        context = {
            'form': formEndereco,
            'cpf': cpf,
            'cidade': cidade,
            'bairro': bairro,
            'rua': rua,
            'numero': numero,
            'complemento': complemento,
            'cep': cep,
        }
        return render(request, "templates/Admin/editar_endereco.html", context)
    
    else:
        msg = 'Erro!'

        context = {
            'msg': msg
        } 
        return render(request, "templates/Admin/mensagem_error.html")

#Deletar endereço
def DeletarEndereco(request):
    if request.method == "GET":
        form = cep_numeroForm()

        context = {
            'form': form
        }
        teste.A = True
        return render(request, "templates/Admin/busca_endereco_delete.html", context)

    elif request.method == 'POST':
        if teste.A:
            teste.A = False
            confirm_delete = get_confirm_delete(request)
            return confirm_delete
        else:
            form = EnderecoForm(request.POST)
            cep = str(request.POST.get('Cep'))
            numero = str(request.POST.get('Numero'))
            endereco = Endereco.objects.all().filter(cep=cep).filter(numero=numero).get()
            endereco.delete()
            return redirect("/Inicio")

#Função para visualizar os dados do cliente            
def Visualizar_Dados_Clientes(request, **kwargs):
    id = descompactar_id(kwargs)

    if request.method == "GET":
        dados = Cliente.objects.all().filter(id_cliente=id)
        dados_endereco = Endereco.objects.all().filter(cliente_id=id)
        cpf = dados.values_list('cpf', flat=True)
        cpf = descompactar_string(cpf, 'cpf')
        nome = descompactar_string(dados, 'nome')
        email = descompactar_string(dados, 'email')
        telefone = descompactar_string(dados, 'telefone')
        sexo = descompactar_string(dados, 'sexo')
        nascimento = descompactar_string(dados, 'data_nascimento')
        nascimento = datetime.strftime(nascimento, '%d/%m/%Y')
        enderecos = list()

        if AEntidadeExiste(dados_endereco):

            cep = descompactar_string(dados_endereco, 'cep')
            numero = descompactar_string(dados_endereco, 'numero')
            valor_consumo = consulta_firebase_consumo(numero, cep)
            dados_endereco.update(consumo_total=valor_consumo)
        else:
            valor_consumo = 0
            dados_endereco.update(consumo_total=valor_consumo)

        for e in dados_endereco:
            endereco = {
                'cidade': e.cidade,
                'bairro': e.bairro,
                'rua': e.rua,
                'numero': e.numero,
                'complemento': e.complemento,
                'cep': e.cep,
                'consumo_total': e.consumo_total,
                'consumo_ultimo_mes': e.consumo_ultimo_mes
            }
            enderecos.append(endereco)

        context = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone,
            'email': email,
            'sexo': sexo,
            'nascimento': nascimento,
            'enderecos': enderecos
        }
        return render( request, "templates/Admin/dados_cliente.html", context)

def Dados_Fatura():
    mes = int(date.today().month)
    ano = int(date.today().year)

    dados_endereco = Endereco.objects.all()
    
    for endereco in dados_endereco:
        x=0
        if len(dados_endereco) >= 1:
            cep = descompactar_string(dados_endereco, 'cep')
            numero = descompactar_string(dados_endereco, 'numero')
            endereco.consumo_total = consulta_firebase_consumo(numero, cep)
            x = endereco.consumo_inicio_mes
            endereco.consumo_inicio_mes = consulta_firebase_consumo(numero, cep)
        else:
            endereco.consumo_total = 0
        
        resultado_total = (abs(endereco.consumo_total) - abs(x))
        endereco.consumo_ultimo_mes = abs(resultado_total)
        cliente = Cliente.objects.all().filter(id_cliente=endereco.cliente_id)
        cliente_nome = descompactar_string(cliente, 'nome')
        fatura = Fatura()
        fatura.cliente = CreateClientFromQuerySet(cliente)
        fatura.consumo_mensal = endereco.consumo_ultimo_mes
        fatura.ano = ano
        fatura.mes = mes
        fatura.endereco = CreateEnderecoFromQuerySet(endereco)
        fatura.valor_pagar = Valor_a_Pagar(fatura.consumo_mensal)
        fatura.fatura_paga = False
        fatura.fatura_nome = cliente_nome
        fatura.cliente.save()
        endereco.save()
        fatura.save()

class FaturaList(ListView):
    template_name = "templates/Admin/lista_de_faturas.html"
    model = Cliente

    def get_queryset(self):
        text_cpf = self.request.GET.get('Cpf')
        text_mes = self.request.GET.get('Mes')
        text_ano = self.request.GET.get('Ano')

        cliente = Cliente.objects.all().filter(cpf=text_cpf)

        if AEntidadeExiste(cliente):
            id = descompactar_string(cliente, "id_cliente")
            fatura = Fatura.objects.all().filter(cliente_id=id).filter(mes = text_mes).filter(ano=text_ano)
        else:
            fatura = Fatura.objects.all()           
        return fatura
       
class teste:
    A = False

def cep_numero(request):
    if request.method == "GET":
        form = cep_numeroForm()
        context = {
            'form': form
        }
        teste.A = True
        return render(request, "templates/Admin/busca_cep_endereco.html", context)

    elif request.method == "POST":
        if teste.A:
            teste.A = False
            editar = editarEndereco(request)
            return editar       
        else:
            teste.A = True
            salvar = salvar_novo_CPF_banco_dados(request)
            return salvar


def execution():
    while True:
        dia_atual = date.today()
        ultimo_dia = dia_atual.replace(monthrange(dia_atual.year, dia_atual.month)[1])
        hora = datetime.now().hour
        minuto = datetime.now().minute
        segundos = datetime.now().second
        if dia_atual == ultimo_dia and hora == 0 and minuto == 0 and segundos == 0:
            Dados_Fatura()
        sleep(86.400)#86.400 = 3600 * 24

#Criação de fatura executando em segundo plano
threading.Thread(target=execution).start()