from django.urls import path
from . import views

urlpatterns = [
    # URLs para Coches
    path('nuevo-coche/', views.NuevoCocheView.as_view(), name='nuevo_coche'),
    path('listado-coches/', views.ListadoCochesView.as_view(), name='listado_coches'),
    path('modificar-coche/<str:matricula>/', views.ModificarCocheView.as_view(), name='modificar_coche'),
    path('eliminar-coche/<str:matricula>/', views.EliminarCocheView.as_view(), name='eliminar_coche'),

    # URLs para Parkings y plazas
    path('nuevo-parking/', views.NuevoParkingView.as_view(), name='nuevo_parking'),
    path('listado-parkings/', views.ListadoParkingsView.as_view(), name='listado_parkings'),
    path('modificar-parking/<int:pk>/', views.ModificarParkingView.as_view(), name='modificar_parking'),
    path('eliminar-parking/<int:pk>/', views.EliminarParkingView.as_view(), name='eliminar_parking'),
    path('parking/<int:pk>/ver/', views.VerParkingView.as_view(), name='ver_parking'),
    path('eliminar-plaza/<int:pk>/<int:plaza_pk>/', views.EliminarPlazaView.as_view(), name='eliminar_plaza'),

    # URLs para otras funcionalidades
    path('nueva-entrada/', views.NuevaEntradaView.as_view(), name='nueva_entrada'),
    path('nueva-salida/', views.NuevaSalidaView.as_view(), name='nueva_salida'),
    path('estadisticas/', views.EstadisticasParkingView.as_view(), name='estadisticas_parking'),

    # URL para la creación de una nueva plaza (ahora recibe el pk del parking)
    path('nueva-plaza/<int:pk>/', views.NuevaPlazaView.as_view(), name='nueva_plaza'),

    # URL para la salida de una plaza específica
    path('parking/<int:pk>/plaza/<int:plaza_pk>/salida/', views.SalidaPlazaView.as_view(), name='salida_plaza'),

    # URL para gestión de usuarios
    path('gestion-usuarios/', views.GestionUsuariosView.as_view(), name='gestion_usuarios'),

    # URL para la creación de un nuevo usuario
    path('nuevo-usuario/', views.NuevoUsuarioView.as_view(), name='nuevo_usuario'),

    # URL para acceso no autorizado
    path('no-autorizado/', views.no_autorizado, name='no_autorizado'),
]