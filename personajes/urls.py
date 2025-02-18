from django.urls import path
from .views import PersonajeDetalles, PersonajeList
from .views import CrearPersonajeView

urlpatterns = [
    path("lista/", PersonajeList.as_view(), name="personaje_list"),
    path("<int:pk>/", PersonajeDetalles.as_view(), name="personaje_detalles"),
    path("crear/", CrearPersonajeView.as_view(), name="crear_personaje"),
]