from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import FormView, CreateView

from .models import Arma, Armadura
from personajes.models import Personaje, InventarioItem
from .forms import ArmaForm, AtaqueFormSet


class EquiparArma(View):
    template_name = "add_equipamiento.html"

    def get(self, request):
        personajes = Personaje.objects.all()
        armas = Arma.objects.filter(inventarioitem__isnull=False)  # Solo armas en inventarios
        return render(request, self.template_name, {"personajes": personajes, "armas": armas})

    def post(self, request):
        personaje_id = request.POST.get("personaje")
        arma_id = request.POST.get("objeto")

        personaje = get_object_or_404(Personaje, id=personaje_id)
        arma = get_object_or_404(Arma, id=arma_id)

        # Verificar si el personaje tiene el arma en su inventario
        if InventarioItem.objects.filter(inventario=personaje.inventario, item_instancia__object_id=arma.id).exists():
            personaje.arma_equipada = arma
            personaje.save()
            messages.success(request, f"{personaje.nombre} ha equipado {arma.nombre}.")
        else:
            messages.error(request, "El personaje no tiene esta arma en su inventario.")

        return redirect("equipar_arma")


class EquiparArmadura(View):
    template_name = "add_equipamiento.html"

    def get(self, request):
        personajes = Personaje.objects.all()
        armaduras = Armadura.objects.filter(inventarioitem__isnull=False)
        return render(request, self.template_name, {"personajes": personajes, "armaduras": armaduras})

    def post(self, request):
        personaje_id = request.POST.get("personaje")
        armadura_id = request.POST.get("objeto")

        personaje = get_object_or_404(Personaje, id=personaje_id)
        armadura = get_object_or_404(Armadura, id=armadura_id)

        if InventarioItem.objects.filter(inventario=personaje.inventario, item_instancia__object_id=armadura.id).exists():
            personaje.armadura_equipada = armadura
            personaje.save()
            messages.success(request, f"{personaje.nombre} ha equipado {armadura.nombre}.")
        else:
            messages.error(request, "El personaje no tiene esta armadura en su inventario.")

        return redirect("equipar_armadura")


class EquipamientoList(View):
    template_name = "equipamiento_list.html"

    def get(self, request):
        armas = Arma.objects.all()
        armaduras = Armadura.objects.all()
        return render(request, self.template_name, {"armas": armas, "armaduras": armaduras})


class ArmaCreateView(CreateView):
    model = Arma
    form_class = ArmaForm
    template_name = 'crear_arma.html'
    success_url = reverse_lazy('equipamiento:equipamiento_list')  # Cambia esto por la vista de tu lista de armas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AtaqueFormSet(self.request.POST)
        else:
            context['formset'] = AtaqueFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object  # Asigna el arma creada a los ataques
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
