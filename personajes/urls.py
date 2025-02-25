from django.urls import path, include
from .views import PersonajeDetalles, personaje_list
from .views import CrearPersonajeView
from rest_framework.routers import DefaultRouter
from .views import PersonajeViewSet

app_name = 'personajes'
router = DefaultRouter()
router.register(r'personajes', PersonajeViewSet)

urlpatterns = [
    path("lista/", personaje_list, name="personaje_list"),
    path("<int:pk>/", PersonajeDetalles.as_view(), name="personaje_detalles"),
    path("crear/", CrearPersonajeView.as_view(), name="crear_personaje"),
    path("api/", include(router.urls)),
]