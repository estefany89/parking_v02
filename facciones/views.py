from django.views.generic import ListView, DetailView
from .models import Faccion
from personajes.models import Personaje

class FaccionListView(ListView):
    """Vista para mostrar la lista de facciones."""
    model = Faccion
    template_name = 'faccion_list.html'
    context_object_name = 'faccion_list'

class FaccionPersonajesView(DetailView):
    """Vista para mostrar los personajes de una facción específica."""
    model = Faccion
    template_name = 'faccion_personajes.html'
    context_object_name = 'faccion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personajes'] = Personaje.objects.filter(faccion=self.object)
        return context