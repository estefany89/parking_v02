from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase

from personajes.views import (
    PersonajeDetalles,
    personaje_list,
    CrearPersonajeView,
    PersonajeViewSet
)


class PersonajesUrlsTest(TestCase):
    """Test de las URLs para la app personajes."""

    def test_personaje_list_url(self):
        """Pruebo que personaje_list funcione correctamente."""
        url = reverse('personajes:personaje_list')
        self.assertEqual(url, '/personajes/lista/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, personaje_list)
        self.assertEqual(resolver.namespace, 'personajes')
        self.assertEqual(resolver.url_name, 'personaje_list')

    def test_personaje_detalle_url(self):
        """Pruebo personaje_detalle"""
        url = reverse('personajes:personaje_detalles', args=[1])
        self.assertEqual(url, '/personajes/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, PersonajeDetalles)
        self.assertEqual(resolver.namespace, 'personajes')
        self.assertEqual(resolver.url_name, 'personaje_detalles')

    def test_crear_personaje_url(self):
        """Pruebo crear_personaje"""
        url = reverse('personajes:crear_personaje')
        self.assertEqual(url, '/personajes/crear/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, CrearPersonajeView)
        self.assertEqual(resolver.namespace, 'personajes')
        self.assertEqual(resolver.url_name, 'crear_personaje')


class PersonajesApiUrlsTest(APITestCase):
    """Tests de la API de personajes."""

    def test_api_root_url(self):
        """Pruebo la url de la API de personajes."""
        url = reverse('personajes:personaje-list')
        self.assertEqual(url, '/personajes/api/personajes/')
        resolver = resolve(url)
        self.assertEqual(
            resolver.func.cls.__name__,
            PersonajeViewSet.__name__
        )

    def test_api_detail_url(self):
        """Pruebo la url de la API con los detalles de personajes."""
        url = reverse('personajes:personaje-detail', args=[1])
        self.assertEqual(url, '/personajes/api/personajes/1/')
        resolver = resolve(url)
        self.assertEqual(
            resolver.func.cls.__name__,
            PersonajeViewSet.__name__
        )