from InterfaceWeb.forms import cep_numeroForm, EnderecoForm,cadastrarForm, loginForm
from InterfaceWeb.models import Endereco, Cliente, InterfaceWebUser
from django.shortcuts import render, redirect
from main.firebase import database
from django.http import HttpResponseRedirect


#Verifica se uma entidade de dados existe ou não
def AEntidadeExiste(querySentCient):
    return len(querySentCient) == 1

#Função para salvar dados de cep e numero da residência no Firebase
def Salvar_no_Firebase(endereco_numero, endereco_cep):
    valor_consumo = 0
    cep_numero = f'{endereco_cep}-{endereco_numero}'

    data = {
        'Litros': valor_consumo
    }
    database.child("Enderecos").child(cep_numero).set(data)

#Descompacta um string, tirando-o de uma lista, o transformando em um único valor
def descompactar_string(variavel, coluna):
    variavel = variavel.values_list(coluna,flat=True)
    variavel = list(variavel)
    variavel = variavel[0]
    return variavel

#Descompactar o id, o retirando de uma lista
def descompactar_id(variavel):
    variavel = variavel.values()
    variavel = list(variavel)
    variavel = variavel[0]
    return variavel

#Confirma a funcionalidade de deletar um endereço
def get_confirm_delete(request):
    form = cep_numeroForm(request.POST)
    text_cep = form['cep'].data
    text_num = form['numero'].data
    cep_numeroDados = Endereco.objects.all().filter(cep=text_cep).filter(numero=text_num)

    if len(cep_numeroDados) == 1:
        id = descompactar_string(cep_numeroDados, "cliente")
        cliente = Cliente.objects.all().filter(id_cliente=id)
        cpf = descompactar_string(cliente, "cpf")
        cidade = descompactar_string(cep_numeroDados, "cidade")
        bairro = descompactar_string(cep_numeroDados, "bairro")
        rua = descompactar_string(cep_numeroDados, "rua")
        numero = descompactar_string(cep_numeroDados, "numero")
        complemento = descompactar_string(cep_numeroDados, "complemento")
        cep = descompactar_string(cep_numeroDados, "cep")
        cliente_id = descompactar_string(cep_numeroDados, "cliente_id")

        formEndereco = EnderecoForm()

        context = {
            'form': formEndereco,
            'cliente_id': cliente_id,
            'cpf': cpf,
            'cidade': cidade,
            'bairro': bairro,
            'rua': rua,
            'numero': numero,
            'complemento': complemento,
            'cep': cep,
        }
        return render(request, "templates/Admin/dados_endereco_delete.html", context)
    else:
        msg = 'Este endereço não foi encontrado!'

        context = {
            'msg': msg
        }
        return render(request, "templates/Admin/mensagem_error.html", context)
    

def consulta_firebase_consumo(endereco_numero, endereco_cep):

    valor_consumo = 0
    cep_numero = f'{endereco_cep}-{endereco_numero}'

    data ={
        'Litros': valor_consumo
    }
    valor_consumo = database.child('Enderecos').child(cep_numero).get(data).val()

    if valor_consumo == None:
        valor_consumo = 0
    else:
        valor_consumo = descompactar_id(valor_consumo)
    
    return valor_consumo


def CreateClientFromQuerySet(querySet):
    client = Cliente()
    client.id_cliente = descompactar_string(querySet, "id_cliente")
    client.cpf = descompactar_string(querySet, "cpf")
    client.nome = descompactar_string(querySet, "nome")
    client.data_nascimento = descompactar_string(querySet, "data_nascimento")
    client.sexo = descompactar_string(querySet, "sexo")
    client.email = descompactar_string(querySet, "email")
    client.telefone = descompactar_string(querySet, "telefone")
    client.save()
    return client

def CreateEnderecoFromQuerySet(querySet):
    endereco = Endereco()
    endereco.id_endereco = querySet.id_endereco
    endereco.cliente_id = querySet.cliente_id
    cliente = Cliente.objects.all().filter(id_cliente=endereco.cliente_id)
    endereco.cliente = CreateClientFromQuerySet(cliente)
    endereco.cidade = querySet.cidade
    endereco.bairro = querySet.bairro
    endereco.rua = querySet.rua
    endereco.numero = querySet.numero
    endereco.complemento = querySet.complemento
    endereco.cep = querySet.cep
    endereco.consumo_total = querySet.consumo_total
    endereco.consumo_ultimo_mes = querySet.consumo_ultimo_mes
    endereco.save()
    return endereco


def Valor_a_Pagar(consumo_atual):

    agua = 44.03
    esgoto = 32.22
    consumo_a_mais = (consumo_atual - 10000)/1000

    if consumo_atual <= 10000:
        valor_pagar = agua + esgoto
    elif consumo_atual > 10000  and  consumo_atual <= 20000:
        valor_pagar = ((consumo_a_mais * 5.68) + agua)  + (esgoto + (consumo_a_mais * 4.54))
    elif consumo_atual  > 20000 and consumo_atual <= 30000:
        valor_pagar = ((consumo_a_mais * 7.49) + agua)  + (esgoto + (consumo_a_mais * 6.74))
    else:
        valor_pagar = ((consumo_a_mais * 10.17) + agua)  + (esgoto + (consumo_a_mais * 10.17))
    
    valor_pagar = round(valor_pagar, 2)
    return valor_pagar

def salvar_novo_CPF_banco_dados(request):

    if request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            cpf = str(request.POST.get('Cpf'))
            cep = str(request.POST.get('Cep'))
            numero = str(request.POST.get('Numero'))
            clientQuerySet = Cliente.objects.all().filter(cpf=cpf)
            if AEntidadeExiste(clientQuerySet) >= 1: 
                endereco = Endereco.objects.all().filter(cep=cep).filter(numero=numero).get()
                endereco.cidade = str(request.POST.get('Cidade'))
                endereco.bairro = str(request.POST.get('Bairro'))
                endereco.rua = str(request.POST.get('Rua'))
                endereco.numero = str(request.POST.get('Numero'))
                endereco.complemento = str(request.POST.get('Complemento'))
                endereco.cep = str(request.POST.get('Cep'))
                endereco.cliente = CreateClientFromQuerySet(clientQuerySet)
                endereco.cliente_id = descompactar_string(clientQuerySet,"id_cliente")
                endereco.save()

                return HttpResponseRedirect("/ListarClientes")
            else:
                msg = 'ERRO!'

                context = {
                    'msg': msg
                }
                return render(request,"templates/Admin/mensagem_error.html", context)    
        else:
            msg = 'ERRO!'

            context = {
                'msg': msg
            }
            return render(request,"templates/Admin/mensagem_error.html", context)  
    else:
            return render(request,"templates/Admin/mensagem_error.html") 
    

def Administrador_Root():
    administrador = InterfaceWebUser.objects.all()
    
    if len(administrador) == 0:
        Administrador = InterfaceWebUser()
        Administrador.cpf = "1234567892"
        Administrador.nome = "Tiago Felipe Rodrigues"
        Administrador.login = "tiagofelipe@gmail.com"
        Administrador.senha = "1234"
        Administrador.save()


def Registrar_Administrador(request):
    if request.method == "GET":
        form = cadastrarForm()
        context = {
            'form':form
        }
        return render(request, "templates/cadastrar_Administrador.html", context)
    
    elif request.method == "POST":
        form = cadastrarForm(request.POST)
        if form.is_valid():
            cpf = form['cpf'].data
            clientQuerySet = InterfaceWebUser.objects.all().filter(cpf=cpf)
            if AEntidadeExiste(clientQuerySet) == False:
                Administrador = InterfaceWebUser()
                Administrador.cpf = form['cpf'].data
                Administrador.nome = form['nome'].data
                Administrador.login = form['login'].data
                Administrador.senha = form['senha'].data
                Administrador.save()

                return redirect('/loginAdministrador')
            
            else:
                msg = 'Este CPF já existe no Banco de Dados. Por favor insira outro CPF!'

                context = {
                    'msg': msg
                }
                return render(request, "templates/Admin/mensagem_error.html")
        
        else:
            msg = 'Error!'

            context = {
                'msg': msg
            }
            return render(request, "templates/Admin/mensagem_error.html")
    else:
        msg = 'Error'

        context = {
            'msg': msg
        }
        return render(request, "templates/Admin/mensagem_error.html")


def Acessar_Login(request):
    #Chamada da função que cria o administrador ROOT
    Administrador_Root()

    if request.method == "GET":
        form = loginForm()
        context = {
            'form': form
        }
        return render(request, "templates/login_administrador.html", context)
    
    elif request.method == "POST":
        form = loginForm(request.POST)
        login = form['login'].data
        senha = form['senha'].data

        if form.is_valid():
            administrador = InterfaceWebUser.objects.all().filter(login=login).filter(senha=senha)
            if len(administrador) == 1:
                login_banco = descompactar_string(administrador, 'login')
                senha_banco = descompactar_string(administrador, 'senha')

                if login == login_banco and senha == senha_banco:
                    return redirect('/Inicio')
                
                else:
                    return render(request, "templates/sem_usuario.html")
            else:
                msg = 'Este usuário não foi encontrado!'

                context = {
                    'msg': msg
                }
                return render(request, "templates/Admin/mensagem_error.html", context)
        else:
            msg = 'Este usuário não foi encontrado!'
            context = {
                'msg': msg
            }
            return render(request, "templates/Admin/mensagem_error.html", context)

    else:
        msg = 'Este usuário não foi encontrado!'
        context = {
            'msg': msg
        }
        return render(request, "templates/Admin/mensagem_error.html", context)



def Login_Administrador(request):

    if request.method == "GET":
        form = loginForm()
        context = {
            'form': form
        }
        return render(request, "templates/login_novo_administrador.html", context)
    
    elif request.method == "POST":
        form = loginForm(request.POST)
        login = form['login'].data
        senha = form['senha'].data

        if form.is_valid():
            administrador = InterfaceWebUser.objects.all().filter(login=login).filter(senha=senha)
            if len(administrador) == 1:
                login_banco = descompactar_string(administrador, 'login')
                senha_banco = descompactar_string(administrador, 'senha')

                if login == login_banco and senha == senha_banco:
                    return redirect('/RegistrarAdministrador')
                
                else:
                    return render(request, "templates/sem_usuario.html")
            else:
                msg = 'Este usuário não foi encontrado!'

                context = {
                    'msg': msg
                }
                return render(request, "templates/Admin/mensagem_error.html", context)
        else:
            msg = 'Este usuário não foi encontrado!'
            context = {
                'msg': msg
            }
            return render(request, "templates/Admin/mensagem_error.html", context)

    else:
        msg = 'Este usuário não foi encontrado!'
        context = {
            'msg': msg
        }
        return render(request, "templates/Admin/mensagem_error.html", context)



    