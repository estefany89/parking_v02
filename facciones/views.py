from django.views.generic import ListView, DetailView
from .models import Faccion
from personajes.models import Personaje
from .serializers import FaccionSerializer
from rest_framework import viewsets
from django.shortcuts import render

class FaccionPersonajesView(DetailView):
    """Vista para mostrar los personajes de una facción específica."""
    model = Faccion
    template_name = 'faccion_personajes.html'
    context_object_name = 'faccion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personajes'] = Personaje.objects.filter(faccion=self.object)
        return context

class FaccionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faccion.objects.all()
    serializer_class = FaccionSerializer

def lista_facciones(request):
    return render(request, "faccion_list.html")