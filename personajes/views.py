from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, render
from .forms import PersonajeForm
from .models import Personaje
from .serializers import PersonajeSerializer
from rest_framework import viewsets

class PersonajeDetalles(DetailView):
    model = Personaje
    template_name = "personaje_detalles.html"
    context_object_name = "personaje"

    def get_object(self):
        return get_object_or_404(Personaje, pk=self.kwargs.get("pk"))


class CrearPersonajeView(FormView):
    template_name = "crear_personaje.html"
    form_class = PersonajeForm
    success_url = reverse_lazy("personajes:personaje_list")

    def form_valid(self, form):
        form.save()  # Guarda el personaje si el formulario es válido
        return super().form_valid(form)

class PersonajeViewSet(viewsets.ModelViewSet):
    queryset = Personaje.objects.all()
    serializer_class = PersonajeSerializer

def personaje_list(request):
    return render(request, 'personaje_list.html')
