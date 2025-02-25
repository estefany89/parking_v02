from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.views.generic import FormView, CreateView
from rest_framework.exceptions import ValidationError

from .models import Arma, Armadura, Consumible
from personajes.models import Personaje, InventarioItem, Inventario
from .forms import ArmaForm, AtaqueFormSet


class EquiparArma(View):
    template_name = "add_arma.html"

    def get(self, request):
        personaje_id = request.GET.get('personaje')
        personajes = Personaje.objects.all()
        armas = []

        # Si se selecciona un personaje muestra solo las armas del inventario
        if personaje_id:
            try:
                personaje = Personaje.objects.get(id=personaje_id)
                arma_content_type = ContentType.objects.get_for_model(Arma)
                # Obtengo las armas del inventario
                arma_items = InventarioItem.objects.filter(
                    inventario=personaje.inventario,
                    content_type=arma_content_type
                )
                arma_ids = arma_items.values_list('object_id', flat=True)
                armas = Arma.objects.filter(id__in=arma_ids)
            except Personaje.DoesNotExist:
                pass

        return render(request, self.template_name, {
            "personajes": personajes,
            "armas": armas,
            "personaje_seleccionado": personaje_id
        })

    def post(self, request):
        personaje_id = request.POST.get("personaje")
        arma_id = request.POST.get("objeto")

        personaje = get_object_or_404(Personaje, id=personaje_id)
        arma = get_object_or_404(Arma, id=arma_id)

        # Verifico si tiene el arma
        try:
            personaje.equipar_arma(arma)
            messages.success(request, f"{personaje.nombre} ha equipado {arma.nombre}.")
        except ValidationError as e:
            messages.error(request, str(e))

        # Redirect con el personaje preseleccionado
        return redirect(f"add_arma?personaje={personaje_id}")


class EquiparArmadura(View):
    template_name = "add_armadura.html"

    def get(self, request):
        personaje_id = request.GET.get('personaje')
        personajes = Personaje.objects.all()
        armaduras = []

        # Si selecciono un personaje muestro solo las armaduras del inventario
        if personaje_id:
            try:
                personaje = Personaje.objects.get(id=personaje_id)
                armadura_content_type = ContentType.objects.get_for_model(Armadura)
                # Pillo las armaduras del inventario
                armadura_items = InventarioItem.objects.filter(
                    inventario=personaje.inventario,
                    content_type=armadura_content_type
                )
                armadura_ids = armadura_items.values_list('object_id', flat=True)
                armaduras = Armadura.objects.filter(id__in=armadura_ids)
            except Personaje.DoesNotExist:
                pass

        return render(request, self.template_name, {
            "personajes": personajes,
            "armaduras": armaduras,
            "personaje_seleccionado": personaje_id
        })

    def post(self, request):
        personaje_id = request.POST.get("personaje")
        armadura_id = request.POST.get("objeto")

        personaje = get_object_or_404(Personaje, id=personaje_id)
        armadura = get_object_or_404(Armadura, id=armadura_id)

        # Verifico si tiene la armadura
        try:
            personaje.equipar_armadura(armadura)
            messages.success(request, f"{personaje.nombre} ha equipado {armadura.nombre}.")
        except ValidationError as e:
            messages.error(request, str(e))

        # Redirect con el personaje preseleccionado
        return redirect(f"add_armadura?personaje={personaje_id}")


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
    success_url = reverse_lazy('equipamiento:equipamiento_list')

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

class CrearArmaduraView(CreateView):
    model = Armadura
    template_name = "crear_armadura.html"
    fields = ['nombre', 'defensa']
    success_url = reverse_lazy('equipamiento:equipamiento_list')


class AnadirItemInventario(View):
    template_name = "anadir_item_inventario.html"

    def get(self, request):
        personaje_id = request.GET.get('personaje')
        tipo_item = request.GET.get('tipo_item', 'arma')  # Por defecto muestra armas

        personajes = Personaje.objects.all()
        items = []

        # Determinar qué items mostrar según el tipo seleccionado
        if tipo_item == 'arma':
            # Obtener armas que no estén en ningún inventario
            items_en_inventario = InventarioItem.objects.filter(
                content_type=ContentType.objects.get_for_model(Arma)
            ).values_list('object_id', flat=True)
            items = Arma.objects.exclude(id__in=items_en_inventario)

        elif tipo_item == 'armadura':
            # Obtener armaduras que no estén en ningún inventario
            items_en_inventario = InventarioItem.objects.filter(
                content_type=ContentType.objects.get_for_model(Armadura)
            ).values_list('object_id', flat=True)
            items = Armadura.objects.exclude(id__in=items_en_inventario)

        elif tipo_item == 'consumible':
            # Obtener consumibles que no estén en ningún inventario
            items_en_inventario = InventarioItem.objects.filter(
                content_type=ContentType.objects.get_for_model(Consumible)
            ).values_list('object_id', flat=True)
            items = Consumible.objects.exclude(id__in=items_en_inventario)

        context = {
            "personajes": personajes,
            "items": items,
            "tipo_item": tipo_item,
            "personaje_seleccionado": personaje_id
        }

        return render(request, self.template_name, context)

    def post(self, request):
        personaje_id = request.POST.get("personaje")
        item_id = request.POST.get("item")
        tipo_item = request.POST.get("tipo_item")
        cantidad = int(request.POST.get("cantidad", 1))

        if not all([personaje_id, item_id, tipo_item]):
            messages.error(request, "Todos los campos son requeridos.")
            return redirect(f"{reverse('equipamiento:anadir-item-inventario')}?personaje={personaje_id}&tipo_item={tipo_item}")

        try:
            personaje = Personaje.objects.get(id=personaje_id)

            # Obtener el modelo y objeto correcto según el tipo
            if tipo_item == 'arma':
                content_type = ContentType.objects.get_for_model(Arma)
                item = Arma.objects.get(id=item_id)
                nombre_item = item.nombre
            elif tipo_item == 'armadura':
                content_type = ContentType.objects.get_for_model(Armadura)
                item = Armadura.objects.get(id=item_id)
                nombre_item = item.nombre
            elif tipo_item == 'consumible':
                content_type = ContentType.objects.get_for_model(Consumible)
                item = Consumible.objects.get(id=item_id)
                nombre_item = item.get_tipo_display()
            else:
                messages.error(request, "Tipo de item no válido.")
                return redirect(reverse('equipamiento:anadir-item-inventario'))

            # Verificar si el personaje ya tiene un inventario, si no, crearlo
            if not hasattr(personaje, 'inventario'):
                inventario = Inventario.objects.create(personaje=personaje)
            else:
                inventario = personaje.inventario

            # Verificar si el item ya está en el inventario, si es así, aumentar la cantidad
            item_existente = InventarioItem.objects.filter(
                inventario=inventario,
                content_type=content_type,
                object_id=item_id
            ).first()

            if item_existente:
                item_existente.cantidad += cantidad
                item_existente.save()
                messages.success(
                    request,
                    f"Se ha aumentado la cantidad de {nombre_item} en el inventario de {personaje.nombre}."
                )
            else:
                # Crear nuevo item en el inventario
                nuevo_item = InventarioItem(
                    inventario=inventario,
                    content_type=content_type,
                    object_id=item_id,
                    cantidad=cantidad
                )
                nuevo_item.full_clean()  # Ejecuta las validaciones
                nuevo_item.save()

                messages.success(
                    request,
                    f"Se ha añadido {nombre_item} al inventario de {personaje.nombre}."
                )

            # Corrección en la redirección
            return redirect(f"{reverse('equipamiento:anadir-item-inventario')}?personaje={personaje_id}&tipo_item={tipo_item}")

        except Personaje.DoesNotExist:
            messages.error(request, "El personaje seleccionado no existe.")
        except (Arma.DoesNotExist, Armadura.DoesNotExist, Consumible.DoesNotExist):
            messages.error(request, "El item seleccionado no existe.")
        except ValidationError as e:
            messages.error(request, f"Error de validación: {str(e)}")

        # Corrección en la redirección
        return redirect(f"{reverse('equipamiento:anadir-item-inventario')}?personaje={personaje_id}&tipo_item={tipo_item}")
