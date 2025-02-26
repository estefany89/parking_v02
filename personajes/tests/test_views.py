from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from facciones.models import Faccion
from localizaciones.models import Localizacion
from personajes.models import Personaje


class TestPersonajeDetalles(TestCase):

    def setUp(self):

        # Configuración inicial para las pruebas
        self.factory = RequestFactory()
        self.localizacion = Localizacion.objects.create(
            nombre="Jerez de la Frontera",
            descripcion="Ole la feria"
        )
        self.faccion = Faccion.objects.create(
            nombre="Faccioooooooon",
            descripcion="miau"
        )

        self.personaje = Personaje.objects.create(
            nombre="Test Personaje",
            localizacion=self.localizacion,
            faccion=self.faccion
        )

        self.inventario = self.personaje.inventario

    def test_detalle_personaje_vista(self):

        # Prueba que la vista de detalles muestra correctamente la información del personaje
        url = reverse('personajes:personaje_detalles', kwargs={'pk': self.personaje.pk})
        response = self.client.get(url)

        # Verifica que la respuesta sea exitosa (código 200)
        self.assertEqual(response.status_code, 200)

        # Verifica que el contexto contenga el personaje correcto
        self.assertEqual(response.context['personaje'], self.personaje)

        # Verifica que se use el template correcto
        self.assertTemplateUsed(response, 'personaje_detalles.html')


class TestCrearPersonajeView(TestCase):

    def setUp(self):

        # Configuración inicial para las pruebas
        self.client = Client()

        self.localizacion = Localizacion.objects.create(
            nombre="Murcia",
            descripcion="Si"
        )

        self.faccion = Faccion.objects.create(
            nombre="Faccion de ejemplo",
            descripcion="eeeeeeee"
        )

        self.url = reverse('personajes:crear_personaje')

    def test_get_crear_personaje(self):

        # Prueba que la página de creación de personaje carga correctamente
        response = self.client.get(self.url)

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)

        # Verifica que se use el template correcto
        self.assertTemplateUsed(response, 'crear_personaje.html')

    def test_post_crear_personaje_valido(self):

        # Prueba la creación de un personaje con datos válidos
        datos_personaje = {
            'nombre': 'Vinicius Jr',
            'localizacion': self.localizacion.pk,
            'faccion': self.faccion.pk,
        }

        response = self.client.post(self.url, datos_personaje)

        # Verifica que se redirija
        self.assertEqual(response.status_code, 302)

        # Verifica que el personaje se haya creado en la base de datos
        self.assertTrue(Personaje.objects.filter(nombre='Vinicius Jr').exists())

        # Verifica que redirija a la URL correcta
        self.assertRedirects(response, reverse('personajes:personaje_list'))


class TestPersonajeList(TestCase):

    def setUp(self):

        # Configuración inicial para las pruebas
        self.client = Client()
        self.url = reverse('personajes:personaje_list')

    def test_personaje_list_vista(self):

        # Prueba que la vista de lista de personajes carga correctamente
        response = self.client.get(self.url)

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)

        # Verifica que se use el template correcto
        self.assertTemplateUsed(response, 'personaje_list.html')

