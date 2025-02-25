from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Localizacion
from django.views import View
from personajes.models import Personaje
from .serializers import LocalizacionSerializer

def lista_localizaciones(request):
    return render(request, "localizacion_list.html")

class LocalizacionPersonajes(View):
    template_name = "localizacion_personajes.html"

    def get(self, request, pk):
        """Obtiene la localización y los personajes asociados a ella."""
        localizacion = get_object_or_404(Localizacion, pk=pk)
        personajes = Personaje.objects.filter(localizacion=localizacion)
        return render(request, self.template_name, {"localizacion": localizacion, "personajes": personajes})

class LocalizacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Localizacion.objects.all()
    serializer_class = LocalizacionSerializer