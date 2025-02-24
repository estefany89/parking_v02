from django.shortcuts import render
from .models import Faccion

def lista_facciones(request):
    facciones = Faccion.objects.all()
    return render(request, 'facciones/lista_facciones.html', {'facciones': facciones})