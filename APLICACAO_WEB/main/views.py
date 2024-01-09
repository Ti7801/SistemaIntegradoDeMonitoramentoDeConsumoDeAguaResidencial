from django.shortcuts import render


def index(request):

    #Renderização da página inicial!

    return render(request, 'templates/index.html')


