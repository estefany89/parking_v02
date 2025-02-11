from django.urls import path
from .views import PersonajeDetalles, PersonajeList
from .views import CrearPersonajeView  # Asegúrate de tener esta vista en views.py

urlpatterns = [
    path("personajes/", PersonajeList.as_view(), name="personaje_list"),
    path("personajes/<int:pk>/", PersonajeDetalles.as_view(), name="personaje_detalles"),
    path("personajes/crear/", CrearPersonajeView.as_view(), name="crear_personaje"),
]