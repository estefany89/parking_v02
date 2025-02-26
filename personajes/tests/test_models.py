from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from equipamiento.models import Armadura, Arma, Consumible
from facciones.models import Faccion
from localizaciones.models import Localizacion
from personajes.models import Personaje, InventarioItem


class PersonajeModelTest(TestCase):

    def setUp(self):
        # Crear otros modelos necesarios
        self.localizacion = Localizacion.objects.create(
            nombre="Madrid",
            descripcion="Bocadillo de calamares"
        )
        self.faccion = Faccion.objects.create(
            nombre="JavaScriptHaters",
            descripcion="Si"
        )

        # Crear equipamiento para probarlo
        self.arma = Arma.objects.create(
            nombre="Espada",
            dano_base=10,
            tipo="espada"
        )
        self.armadura = Armadura.objects.create(
            nombre="Casco",
            defensa=5
        )

        # Personaje de prueba
        self.personaje = Personaje.objects.create(
            nombre="Test Personaje",
            localizacion=self.localizacion,
            faccion=self.faccion,
            hp=100
        )

        self.inventario = self.personaje.inventario

    def test_personaje_creation(self):
        """Test de creacion de personaje"""
        self.assertEqual(self.personaje.nombre, "Test Personaje")
        self.assertEqual(self.personaje.localizacion, self.localizacion)
        self.assertEqual(self.personaje.faccion, self.faccion)
        self.assertEqual(self.personaje.hp, 100)
        self.assertIsNone(self.personaje.arma_equipada)
        self.assertIsNone(self.personaje.armadura_equipada)

    def test_str_method(self):
        """Test del string de personaje"""
        self.assertEqual(str(self.personaje), "Test Personaje")

    def test_equipar_arma_success(self):
        """Test equipar arma del inventario"""
        # Añadir arma al inventario
        arma_ct = ContentType.objects.get_for_model(self.arma)
        InventarioItem.objects.create(
            inventario=self.inventario,
            content_type=arma_ct,
            object_id=self.arma.id,
            cantidad=1
        )

        # Equipar
        self.personaje.equipar_arma(self.arma)

        # Miro si está equipada
        self.assertEqual(self.personaje.arma_equipada, self.arma)

    def test_equipar_arma_failure(self):
        """Compruebo que equipar un arma que no esté en el inventario de error"""
        # Try to equip a weapon that's not in the inventory
        with self.assertRaises(ValidationError):
            self.personaje.equipar_arma(self.arma)

    def test_equipar_armadura_success(self):
        """Pruebo las armaduras del inventario"""
        # Añadir armadura al inventario
        armadura_ct = ContentType.objects.get_for_model(self.armadura)
        InventarioItem.objects.create(
            inventario=self.inventario,
            content_type=armadura_ct,
            object_id=self.armadura.id,
            cantidad=1
        )

        # Equipar
        self.personaje.equipar_armadura(self.armadura)

        # Compruebo
        self.assertEqual(self.personaje.armadura_equipada, self.armadura)

    def test_equipar_armadura_failure(self):
        """Test para armadura que no está en el inventario"""
        with self.assertRaises(ValidationError):
            self.personaje.equipar_armadura(self.armadura)

    def test_desequipar_arma(self):
        """Test para desequipar"""
        # Primero equipo
        arma_ct = ContentType.objects.get_for_model(self.arma)
        InventarioItem.objects.create(
            inventario=self.inventario,
            content_type=arma_ct,
            object_id=self.arma.id,
            cantidad=1
        )
        self.personaje.equipar_arma(self.arma)

        # Pruebo desequipar
        self.personaje.desequipar_arma()

        # Compruebo que va bien
        self.assertIsNone(self.personaje.arma_equipada)

    def test_desequipar_armadura(self):
        """Desequipar armadura"""
        # Primero la equipo
        armadura_ct = ContentType.objects.get_for_model(self.armadura)
        InventarioItem.objects.create(
            inventario=self.inventario,
            content_type=armadura_ct,
            object_id=self.armadura.id,
            cantidad=1
        )
        self.personaje.equipar_armadura(self.armadura)

        # Ahora pruebo desequipar
        self.personaje.desequipar_armadura()

        # Compruebo
        self.assertIsNone(self.personaje.armadura_equipada)


class InventarioItemModelTest(TestCase):

    def setUp(self):
        # Objetos necesarios
        self.localizacion = Localizacion.objects.create(
            nombre="Granada",
            descripcion="Ole"
        )
        self.faccion = Faccion.objects.create(
            nombre="Estefany",
            descripcion="aaaaaaaaaaaaa"
        )

        self.personaje = Personaje.objects.create(
            nombre="Test Personaje",
            localizacion=self.localizacion,
            faccion=self.faccion
        )

        self.inventario = self.personaje.inventario

        self.arma = Arma.objects.create(
            nombre="Espada",
            dano_base=10,
            tipo="espada"
        )
        self.armadura = Armadura.objects.create(
            nombre="Pechera",
            defensa=5
        )
        self.consumible = Consumible.objects.create(
            tipo=Consumible.VIDA,
            potencia=20
        )

    def test_add_arma_to_inventory(self):
        """Añadir arma al inventario"""
        arma_ct = ContentType.objects.get_for_model(self.arma)
        item = InventarioItem.objects.create(
            inventario=self.inventario,
            content_type=arma_ct,
            object_id=self.arma.id,
            cantidad=2
        )

        self.assertEqual(item.item, self.arma)
        self.assertEqual(item.cantidad, 2)
        self.assertEqual(str(item), f"2x {self.arma}")

    def test_add_armadura_to_inventory(self):
        """Añadir armadura al inventario"""
        armadura_ct = ContentType.objects.get_for_model(self.armadura)
        item = InventarioItem.objects.create(
            inventario=self.inventario,
            content_type=armadura_ct,
            object_id=self.armadura.id,
            cantidad=1
        )

        self.assertEqual(item.item, self.armadura)
        self.assertEqual(item.cantidad, 1)

    def test_add_consumible_to_inventory(self):
        """Añadir consumible al inventario"""
        consumible_ct = ContentType.objects.get_for_model(self.consumible)
        item = InventarioItem.objects.create(
            inventario=self.inventario,
            content_type=consumible_ct,
            object_id=self.consumible.id,
            cantidad=5
        )

        self.assertEqual(item.item, self.consumible)
        self.assertEqual(item.cantidad, 5)

    def test_inventory_item_validation(self):
        """Compruebo que solo se añadan los objetos correctos"""
        # Creo InventarioItem con objeto valido
        inventario_item = InventarioItem(
            inventario=self.inventario,
            content_type=ContentType.objects.get_for_model(self.arma),
            object_id=self.arma.id,
            cantidad=1
        )

        inventario_item.clean()


class InventarioModelTest(TestCase):

    def setUp(self):
        # Creo objetos necesarios
        self.localizacion = Localizacion.objects.create(
            nombre="Francia",
            descripcion="Mierdon"
        )
        self.faccion = Faccion.objects.create(
            nombre="API",
            descripcion="dddddddddddd"
        )

        self.personaje = Personaje.objects.create(
            nombre="Test Personaje",
            localizacion=self.localizacion,
            faccion=self.faccion
        )

        self.inventario = self.personaje.inventario


    def test_str_method(self):
        """Pruebo el string de personaje"""
        self.assertEqual(str(self.inventario), "Inventario de Test Personaje")

    def test_inventario_personaje_relationship(self):
        """Pruebo que el personaje tenga un inventario relacionado"""
        self.assertEqual(self.personaje.inventario, self.inventario)