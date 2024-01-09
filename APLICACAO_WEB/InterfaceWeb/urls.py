from django.urls import path
from . import views
from InterfaceWeb import funcoes
from InterfaceWeb import views
from main.views import index

app_name = 'InterfaceWeb'

urlpatterns = [
    path('', funcoes.Acessar_Login, name="login"),
    path('LoginAdmin/', funcoes.Login_Administrador, name="loginAdministrador"),  
    path('RegistrarAdministrador/', funcoes.Registrar_Administrador, name="registrar"),
    path('Inicio/', index, name="inicio"),
    path('ListarClientes/', views.ClienteList.as_view(), name="listaClientes"),
    path('ListarFaturas/', views.FaturaList.as_view(), name="listaFaturas"),
    path('CriarCliente/', views.ClienteCreate.as_view(), name="criarCliente"),
    path('CriarEndereco/', views.CriarEndereco, name="criarEndereco"),
    path('EditarCliente/<int:pk>/', views.ClienteUpdate.as_view(),name="editarCliente"),
    path('BuscaCEPNumero/',views.cep_numero, name="buscaCepNumero"),
    path('DeletarEndereco/', views.DeletarEndereco, name="buscaDeletarEndereco"),
    path('DetalhesCliente/<int:pk>/', views.Visualizar_Dados_Clientes, name="detalhes"),
    path('DeletarCliente/<int:pk>/', views.ClienteDelete.as_view(), name="deletarCliente")
]
