from django.urls import path
from .views import EquiparArma, EquiparArmadura, EquipamientoList, ArmaCreateView

app_name = "equipamiento"
urlpatterns = [
    path("equipar_arma/", EquiparArma.as_view(), name="equipar_arma"),
    path("equipar_armadura/", EquiparArmadura.as_view(), name="equipar_armadura"),
    path("equipamiento/", EquipamientoList.as_view(), name="equipamiento_list"),
    path("crear_arma/", ArmaCreateView.as_view(), name="crear_arma"),
]