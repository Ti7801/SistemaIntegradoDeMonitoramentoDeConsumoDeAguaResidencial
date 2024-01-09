from InterfaceWeb.models import Cliente
from django import forms

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

class EnderecoForm(forms.Form):
    cpf = forms.CharField(label="CPF do cliente", max_length=11, required=False)
    cidade = forms.CharField(label="Cidade", max_length=50, required=False)
    bairro = forms.CharField(label="Bairro", max_length=50, required=False)
    rua = forms.CharField(label="Rua", max_length=50, required=False)
    numero = forms.CharField(label="Numero", max_length=50, required=False)
    complemento = forms.CharField(label="Complemento", max_length=50, required=False)
    cep = forms.CharField(label="Cep", max_length=50, required=False)

class cep_numeroForm(forms.Form):
    cep = forms.CharField(label="CEP", max_length=9, required=False)
    numero = forms.CharField(label="Numero", max_length=5, required=False)

class loginForm(forms.Form):
    login = forms.CharField(label="ID", max_length=50, required=False)
    senha = forms.CharField(label="Senha", max_length=50, required=False)

class cadastrarForm(forms.Form):
    cpf = forms.CharField(label="Cpf", max_length=11, required=False)
    nome = forms.CharField(label="Nome", max_length=50, required=False)
    login = forms.CharField(label="ID", max_length=50, required=False)
    senha = forms.CharField(label="Senha", max_length=50, required=False)
