from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Relacion
from django.urls import reverse_lazy

class RelacionListView(ListView):
    model = Relacion
    template_name = 'relacion_list.html'

class RelacionDetailView(DetailView):
    model = Relacion
    template_name = 'relacion_detail.html'

class RelacionCreateView(CreateView):
    model = Relacion
    fields = ['personaje1', 'personaje2', 'tipo']
    template_name = 'relacion_form.html'
    success_url = reverse_lazy('relaciones:relacion_list')

class RelacionUpdateView(UpdateView):
    model = Relacion
    fields = ['tipo', 'nivel_confianza']
    template_name = 'relacion_form.html'

class RelacionDeleteView(DeleteView):
    model = Relacion
    template_name = 'relacion_confirm_delete.html'
    success_url = '/inicio'