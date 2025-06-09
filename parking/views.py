from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from .models import Vehiculo, Parking
from .models import Plaza
from django.utils import timezone
from .models import RegistroOcupacion
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import PerfilUsuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

# El Mixin  "Requerido ser administrador" 
class AdminRequiredMixin:
    """Mixin para restringir acceso solo a administradores."""
    def dispatch(self, request, *args, **kwargs):
        perfil = getattr(request.user, 'perfilusuario', None)
        if not (request.user.is_authenticated and perfil and perfil.rol == 'admin'):
            return HttpResponseRedirect(reverse('no_autorizado'))
        return super().dispatch(request, *args, **kwargs)


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        perfil = getattr(request.user, 'perfilusuario', None)
        if perfil and perfil.rol == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('no_autorizado')  # Crea una vista/template para acceso denegado
    return _wrapped_view


class NuevoCocheView(View):
    # Muestra el formulario para añadir un nuevo coche
    def get(self, request):
        return render(request, 'parking/nuevo_coche.html', {"mensaje": None, "error": None})

    # Procesa el formulario para añadir un nuevo coche
    def post(self, request):
        mensaje = None
        error = None
        matricula = request.POST.get("matricula")
        marca = request.POST.get("marca")
        modelo = request.POST.get("modelo")
        color = request.POST.get("color")
        propietario_nombre = request.POST.get("propietario_nombre")
        propietario_telefono = request.POST.get("propietario_telefono")

        if matricula and marca and modelo and color and propietario_nombre:
            if not Vehiculo.objects.filter(matricula=matricula).exists():
                Vehiculo.objects.create(
                    matricula=matricula,
                    marca=marca,
                    modelo=modelo,
                    color=color,
                    propietario_nombre=propietario_nombre,
                    propietario_telefono=propietario_telefono
                )
                mensaje = "Coche guardado correctamente."
            else:
                error = "Ya existe un coche con esa matrícula."
        else:
            error = "Todos los campos obligatorios deben estar completos."

        return render(request, 'parking/nuevo_coche.html', {"mensaje": mensaje, "error": error})


class NuevaEntradaView(View):
    def get(self, request):
        parkings = Parking.objects.all()
        parking_id = request.GET.get("parking")
        plaza_numero = request.GET.get("plaza")
        return render(request, 'parking/nueva_entrada.html', {
            "parkings": parkings,
            "parking_id": parking_id,
            "plaza_numero": plaza_numero,
            "mensaje": None,
            "error": None
        })

    def post(self, request):
        mensaje = None
        error = None
        matricula = request.POST.get("matricula")
        parking_id = request.POST.get("parking")
        plaza_numero = request.POST.get("plaza")

        if matricula and parking_id and plaza_numero:
            try:
                coche = Vehiculo.objects.get(matricula=matricula)
            except Vehiculo.DoesNotExist:
                coche = None
            try:
                parking = Parking.objects.get(pk=parking_id)
                plaza = Plaza.objects.get(numero=plaza_numero, parking=parking)
            except (Parking.DoesNotExist, Plaza.DoesNotExist):
                plaza = None

            if coche and plaza:
                # Comprobar si el coche ya está aparcado en cualquier plaza (registro activo)
                registro_activo = RegistroOcupacion.objects.filter(vehiculo=coche, fecha_salida__isnull=True).first()
                if registro_activo:
                    error = "Este coche ya está aparcado en otra plaza y no puede registrarse en otra hasta que salga."
                elif not plaza.ocupada:
                    RegistroOcupacion.objects.create(
                        vehiculo=coche,
                        plaza=plaza,
                        fecha_entrada=timezone.now(),
                        operador_entrada=request.user if request.user.is_authenticated else None,  # Guarda el operador logueado
                        fecha_salida=None
                    )
                    plaza.ocupada = True
                    plaza.save()
                    mensaje = "Entrada registrada correctamente."
                else:
                    error = "La plaza seleccionada ya está ocupada."
            else:
                error = "No se ha encontrado el coche o la plaza."
        else:
            error = "Debe seleccionar un parking, una matrícula y un número de plaza."

        parkings = Parking.objects.all()
        return render(request, 'parking/nueva_entrada.html', {
            "parkings": parkings,
            "mensaje": mensaje,
            "error": error
        })


class NuevaSalidaView(View):
    def get(self, request):
        parkings = Parking.objects.all()
        parking_id = request.GET.get("parking")
        plaza_numero = request.GET.get("plaza")
        return render(request, 'parking/nueva_salida.html', {
            "parkings": parkings,
            "parking_id": parking_id,
            "plaza_numero": plaza_numero,
            "mensaje": None,
            "error": None
        })

    def post(self, request):
        mensaje = None
        error = None
        parking_id = request.POST.get("parking")
        plaza_numero = request.POST.get("plaza")
        parkings = Parking.objects.all()

        try:
            parking = Parking.objects.get(pk=parking_id)
            plaza = Plaza.objects.get(numero=plaza_numero, parking=parking)
        except (Parking.DoesNotExist, Plaza.DoesNotExist):
            plaza = None

        if plaza and plaza.ocupada:
            registro = RegistroOcupacion.objects.filter(plaza=plaza, fecha_salida__isnull=True).order_by('-fecha_entrada').first()
            if registro:
                registro.fecha_salida = timezone.now()
                registro.operador_salida = request.user if request.user.is_authenticated else None  # Guarda el operador logueado
                registro.save()
                plaza.ocupada = False
                plaza.save()
                mensaje = "Salida registrada correctamente."
            else:
                error = "No se encontró un registro de ocupación activo para esta plaza."
        elif plaza:
            error = "La plaza no estaba ocupada, no puede registrar una salida."
        else:
            error = "No se encontró la plaza indicada."

        return render(request, 'parking/nueva_salida.html', {
            "parkings": parkings,
            "parking_id": parking_id,
            "plaza_numero": plaza_numero,
            "mensaje": mensaje,
            "error": error
        })


class EstadisticasParkingView(View):
    def get(self, request):
        parkings = Parking.objects.all()
        parkings_stats = []
        user_stats = []

        for parking in parkings:
            plazas = Plaza.objects.filter(parking=parking)
            num_plazas = plazas.count()
            num_libres = plazas.filter(ocupada=False).count()
            num_ocupadas = plazas.filter(ocupada=True).count()
            porcentaje_ocupacion = (num_ocupadas / num_plazas * 100) if num_plazas > 0 else 0
            parkings_stats.append({
                'nombre': parking.nombre,
                'num_plazas': num_plazas,
                'num_libres': num_libres,
                'porcentaje_ocupacion': porcentaje_ocupacion,
            })

            # Estadísticas de entradas/salidas por usuario actual
            num_entradas = RegistroOcupacion.objects.filter(
                plaza__parking=parking,
                operador_entrada=request.user
            ).count()
            num_salidas = RegistroOcupacion.objects.filter(
                plaza__parking=parking,
                operador_salida=request.user
            ).count()
            user_stats.append({
                'parking_nombre': parking.nombre,
                'num_entradas': num_entradas,
                'num_salidas': num_salidas,
            })

        return render(request, 'parking/estadisticas_parking.html', {
            'parkings': parkings_stats,
            'user_stats': user_stats
        })


class SituacionActualView(View):
    def get(self, request):
        # Lógica para situación actual
        return render(request, 'parking/situacion_actual.html')


class ListadoCochesView(ListView):
    model = Vehiculo
    template_name = 'parking/listado_coches.html'
    context_object_name = 'coches'


class ModificarCocheView(View):
    def get(self, request, matricula=None):
        coche = get_object_or_404(Vehiculo, matricula=matricula) if matricula else None
        return render(request, 'parking/modificar_coche.html', {
            "coche": coche,
            "mensaje": None,
            "error": None
        })

    def post(self, request, matricula=None):
        coche = get_object_or_404(Vehiculo, matricula=matricula) if matricula else None
        mensaje = None
        error = None

        marca = request.POST.get("marca")
        modelo = request.POST.get("modelo")
        color = request.POST.get("color")
        propietario_nombre = request.POST.get("propietario_nombre")
        propietario_telefono = request.POST.get("propietario_telefono")

        if marca and modelo and color and propietario_nombre:
            coche.marca = marca
            coche.modelo = modelo
            coche.color = color
            coche.propietario_nombre = propietario_nombre
            coche.propietario_telefono = propietario_telefono
            coche.save()
            mensaje = "Coche modificado correctamente."
        else:
            error = "Todos los campos obligatorios deben estar completos."

        return render(request, 'parking/modificar_coche.html', {
            "coche": coche,
            "mensaje": mensaje,
            "error": error
        })


class EliminarCocheView(View):
    def get(self, request, matricula):
        coche = get_object_or_404(Vehiculo, matricula=matricula)
        coche.delete()
        return redirect('listado_coches')


# Parking
class NuevoParkingView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'parking/nuevo_parking.html', {"mensaje": None, "error": None})

    def post(self, request):
        mensaje = None
        error = None
        nombre = request.POST.get("nombre")
        ciudad = request.POST.get("ciudad")

        if nombre and ciudad:
            Parking.objects.create(nombre=nombre, ciudad=ciudad)
            mensaje = "Parking guardado correctamente."
        else:
            error = "Todos los campos son obligatorios."

        return render(request, 'parking/nuevo_parking.html', {"mensaje": mensaje, "error": error})


class ListadoParkingsView(ListView):
    model = Parking
    template_name = 'parking/listado_parkings.html'
    context_object_name = 'parkings'


# Parking
class ModificarParkingView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, pk):
        parking = get_object_or_404(Parking, pk=pk)
        return render(request, 'parking/modificar_parking.html', {
            "parking": parking,
            "mensaje": None,
            "error": None
        })

    def post(self, request, pk):
        parking = get_object_or_404(Parking, pk=pk)
        mensaje = None
        error = None

        nombre = request.POST.get("nombre")
        ciudad = request.POST.get("ciudad")

        if nombre and ciudad:
            parking.nombre = nombre
            parking.ciudad = ciudad
            parking.save()
            mensaje = "Parking modificado correctamente."
        else:
            error = "Todos los campos son obligatorios."

        return render(request, 'parking/modificar_parking.html', {
            "parking": parking,
            "mensaje": mensaje,
            "error": error
        })


# Parking
class EliminarParkingView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, pk):
        parking = get_object_or_404(Parking, pk=pk)
        parking.delete()
        return redirect('listado_parkings')

class NuevaPlazaView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, pk):
        parking = get_object_or_404(Parking, pk=pk)
        return render(request, 'parking/nueva_plaza.html', {
            "parking": parking,
            "mensaje": None,
            "error": None
        })

    def post(self, request, pk):
        mensaje = None
        error = None
        numero = request.POST.get("numero")
        parking = get_object_or_404(Parking, pk=pk)

        if numero:
            if not Plaza.objects.filter(numero=numero, parking=parking).exists():
                Plaza.objects.create(numero=numero, parking=parking)
                mensaje = "Plaza creada correctamente."
            else:
                error = "Ya existe una plaza con ese número en este parking."
        else:
            error = "El número de plaza es obligatorio."

        return render(request, 'parking/nueva_plaza.html', {
            "parking": parking,
            "mensaje": mensaje,
            "error": error
        })
    
class VerParkingView(View):
    def get(self, request, pk):
        parking = get_object_or_404(Parking, pk=pk)
        plazas = Plaza.objects.filter(parking=parking).order_by('numero')
        ocupantes = {}
        for plaza in plazas:
            ocupacion = RegistroOcupacion.objects.filter(plaza=plaza, fecha_salida__isnull=True).order_by('-fecha_entrada').first()
            ocupantes[plaza.id] = ocupacion.vehiculo if ocupacion else None

        total_plazas = plazas.count()
        ocupadas = plazas.filter(ocupada=True).count()
        libres = total_plazas - ocupadas

        porcentaje_ocupadas = (ocupadas / total_plazas * 100) if total_plazas > 0 else 0
        porcentaje_libres = (libres / total_plazas * 100) if total_plazas > 0 else 0

        return render(request, 'parking/ver_parking.html', {
            "parking": parking,
            "plazas": plazas,
            "ocupantes": ocupantes,
            "total_plazas": total_plazas,
            "porcentaje_ocupadas": porcentaje_ocupadas,
            "porcentaje_libres": porcentaje_libres
        })
    
# Plaza
@method_decorator([login_required, admin_required], name='dispatch')
class EliminarPlazaView(View):
    def post(self, request, pk, plaza_pk):
        plaza = get_object_or_404(Plaza, pk=plaza_pk, parking_id=pk)
        plaza.delete()
        return redirect('ver_parking', pk=pk)
    
class SalidaPlazaView(View):
    def post(self, request, pk, plaza_pk):
        plaza = get_object_or_404(Plaza, pk=plaza_pk, parking_id=pk)
        registro = RegistroOcupacion.objects.filter(plaza=plaza, fecha_salida__isnull=True).order_by('-fecha_entrada').first()
        if registro:
            registro.fecha_salida = timezone.now()
            registro.operador_salida = request.user if request.user.is_authenticated else None
            registro.save()
            plaza.ocupada = False
            plaza.save()
        return redirect('ver_parking', pk=pk)

# Usuarios
@method_decorator([login_required, admin_required], name='dispatch')
class GestionUsuariosView(View):
    def get(self, request):
        usuarios = PerfilUsuario.objects.select_related('user').all()
        return render(request, 'parking/gestion_usuarios.html', {'usuarios': usuarios})

# Usuarios
@method_decorator([login_required, admin_required], name='dispatch')
class NuevoUsuarioView(View):
    def get(self, request):
        return render(request, 'parking/nuevo_usuario.html', {"mensaje": None, "error": None})

    def post(self, request):
        mensaje = None
        error = None
        username = request.POST.get("username")
        password = request.POST.get("password")
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        rol = request.POST.get("rol")

        if username and password and nombre and rol:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create(
                    username=username,
                    password=make_password(password),
                    first_name=nombre,
                    email=email
                )
                PerfilUsuario.objects.create(user=user, rol=rol)
                mensaje = "Usuario creado correctamente."
            else:
                error = "Ya existe un usuario con ese nombre."
        else:
            error = "Todos los campos obligatorios deben estar completos."

        return render(request, 'parking/nuevo_usuario.html', {"mensaje": mensaje, "error": error})

def no_autorizado(request):
    return render(request, 'parking/no_autorizado.html')

