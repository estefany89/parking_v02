from django.urls import path
from .views import EquiparArma, EquiparArmadura, EquipamientoList, ArmaCreateView, AnadirItemInventario, \
    CrearArmaduraView

app_name = "equipamiento"
urlpatterns = [
    path("equipar_arma/", EquiparArma.as_view(), name="equipar_arma"),
    path("equipar_armadura/", EquiparArmadura.as_view(), name="equipar_armadura"),
    path("equipamiento_list/", EquipamientoList.as_view(), name="equipamiento_list"),
    path("crear_arma/", ArmaCreateView.as_view(), name="crear_arma"),
    path('crear_armadura/', CrearArmaduraView.as_view(), name='crear_armadura'),
    path("anadir-item-inventario/", AnadirItemInventario.as_view(), name="anadir-item-inventario"),
]