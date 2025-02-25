from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Localizacion
from django.views import View
from personajes.models import Personaje

class LocalizacionList(ListView):
    model = Localizacion
    template_name = "localizacion_list.html"
    context_object_name = "localizacion_list"

class LocalizacionPersonajes(View):
    template_name = "localizacion_personajes.html"

    def get(self, request, pk):
        """Obtiene la localización y los personajes asociados a ella."""
        localizacion = get_object_or_404(Localizacion, pk=pk)
        personajes = Personaje.objects.filter(localizacion=localizacion)
        return render(request, self.template_name, {"localizacion": localizacion, "personajes": personajes})