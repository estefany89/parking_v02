# TIERRA MEDIA WEB

Versión web del proyecto hecho anteriormente en python.



## Tech Stack

- **Django**: Framework principal del proyecto.
- **Django REST Framework**: Para la creación de APIs RESTful.
- **Docker**: Para facilitar la configuración y despliegue del proyecto.
- **PostgreSQL**: Base de datos relacional.
- **HTMX**: Para tareas asincrónicas.
- **Pillow**: Para la manipulación de imágenes (como redimensionar las imágenes de los personajes).
- **Bootstrap**: Framework CSS para mejorar la interfaz de usuario.
- **JavaScript**: Para manejo de eventos y API Fetch.


## 🛠 Installación y configuración del proyecto

Para poder probar el proyecto correctamente sigue los siguientes pasos:

1. Clonar el repositorio
```bash
git clone https://github.com/JesusJimenez01/tierra_media_web.git
cd tierra_media_web
```
2. Construir y levantar los contenedores
```bash
docker compose up --build -d
```
3. Aplicar migraciones y cargar datos
```bash
docker compose exec web python manage.py migrate
```
4. Crear un superusuario para poder acceder al admin en caso de querer comprobarlo
```bash
docker compose exec web python manage.py createsuperuser
```
5. Acceder a la aplicación
http://localhost:8000/inicio
    
## 🎮 Estructura del Juego

El proyecto está dividido en diferentes aplicaciones, cada una encargada de una funcionalidad específica:

- **inicio**: Contiene la página principal y navegación general.
- **personajes**: Gestión de personajes, incluyendo creación.
- **localizaciones**: Información sobre los distintos lugares de la Tierra Media y su      relación con los personajes.
- **relaciones**: Define vínculos entre personajes, facciones y eventos.
- **facciones**: Gestión de las diferentes facciones del mundo
- **equipamiento**: Administración de armas, armaduras y del inventario.
- **batalla**: Mecánica de combate, gestión de enfrentamientos y resolución de batallas.


# Inicio
La aplicación **inicio** gestiona la página principal del juego, donde los jugadores pueden acceder a las diferentes secciones del juego a través de un menú.

### 📌 Funcionalidades principales

- **Visualización del menú**: Los jugadores pueden acceder a todas las secciones del juego desde un único menú, que incluye enlaces a las funcionalidades de personajes, equipamiento, localizaciones, facciones y batalla.
- **Accesos directos a cada sección**: El menú contiene enlaces a las vistas más importantes de las aplicaciones relacionadas con personajes, equipamiento, localizaciones, facciones y batallas.

### 🖼 Vista principal

#### `mostrar_menu`
Esta vista renderiza la página principal que contiene el menú del juego. El menú está disponible para los jugadores y les permite navegar entre las diferentes secciones de la aplicación.
# Personajes
La aplicación **personajes** se encarga de la creación, gestión y visualización de los personajes dentro del juego.  

### 📌 Funcionalidades principales

- **Creación de personajes**: A través de un formulario (`CrearPersonajeView`), los jugadores pueden crear un personaje con un nombre, facción y localización inicial.  
- **Inventario**: Cada personaje tiene un inventario (`Inventario`), donde puede almacenar armas, armaduras y consumibles.  
- **Equipamiento**: Los personajes pueden equipar o desequipar armas y armaduras si las poseen en su inventario.  
- **Imágenes**: Las imágenes de los personajes se redimensionan automáticamente a 300x300 px para optimización.  
- **Vistas**:  
  - `PersonajeDetalles (DetailView)`: Muestra los detalles de un personaje específico.  
  - `CrearPersonajeView (FormView)`: Permite la creación de un personaje mediante un formulario.  
  - `PersonajeViewSet (ModelViewSet)`: API para gestionar personajes.  
  - `personaje_list (function view)`: Renderiza una lista de personajes.  
- **Eventos automáticos**:  
  - Cuando se crea un personaje, automáticamente se genera un inventario para él (`crear_inventario`).  

### 📂 Modelos principales

#### `Personaje`
Representa a un personaje en el juego. Atributos clave:
- **Nombre** (`nombre`)
- **Localización** (`localizacion`) → Relacionado con `Localizacion`
- **Facción** (`faccion`) → Relacionado con `Faccion`
- **HP** (`hp`) → Vida del personaje
- **Equipamiento** (`arma_equipada`, `armadura_equipada`)
- **Imagen** (`imagen`) → Se almacena en `/media/personajes/`

Métodos importantes:
- `equipar_arma(arma)`, `equipar_armadura(armadura)`, `desequipar_arma()`, `desequipar_armadura()`
- `redimensionar_imagen()`: Ajusta la imagen a 300x300 px automáticamente.

#### `Inventario`
Cada personaje tiene un inventario donde almacena objetos.  
- `InventarioItem`: Permite guardar armas, armaduras y consumibles.  
- Usa `GenericForeignKey` para manejar diferentes tipos de objetos.

### 🤖 API Endpoints
Mediante `PersonajeViewSet` se exponen los endpoints REST para gestionar personajes.

| Método | Endpoint                          | Descripción |
|--------|-----------------------------------|-------------|
| GET | `personajes/api/personajes/`      | Lista todos los personajes |
| POST | `personajes/api/personajes/`      | Crea un nuevo personaje |
| GET | `personajes/api/personajes/{id}/` | Obtiene detalles de un personaje |
| PUT | `personajes/api/personajes/{id}/` | Modifica un personaje |
| DELETE | `personajes/api/personajes/{id}/` | Elimina un personaje |

### 🖼 Plantillas y Frontend
- `personaje_list.html`: Lista de personajes.
- `personaje_detalles.html`: Página con los detalles de un personaje específico.
- `crear_personaje.html`: Formulario para crear un personaje.
# Equipamiento

El sistema de **Equipamiento** permite a los personajes equipar armas, armaduras y gestionar su inventario.

### 📌 Funcionalidades principales

- **Equipar Arma**: Los personajes pueden equipar un arma de su inventario.  
- **Equipar Armadura**: Los personajes pueden equipar una armadura de su inventario.  
- **Crear Arma**: Los administradores pueden crear armas con diferentes tipos y ataques.  
- **Crear Armadura**: Los administradores pueden crear armaduras con valores de defensa.  
- **Añadir Items al Inventario**: Los personajes pueden añadir armas, armaduras o consumibles a su inventario.

### 📂 Modelos principales

#### `Arma`
Representa un arma que puede ser equipada por los personajes.  
Atributos clave:
- **nombre**: Nombre del arma.
- **dano_base**: Daño base del arma.
- **tipo**: Tipo de arma (espada, hacha, daga, etc.).
- **es_unica**: Si el arma es única en el juego.

Métodos importantes:
- `clean()`: Validación para asegurar que solo haya una copia de un arma única en el juego.

#### `Ataque`
Representa un ataque de un arma.
- **nombre**: Nombre del ataque.
- **dano**: Daño asociado al ataque.
- **arma**: Relacionado con el modelo `Arma`.

#### `Armadura`
Representa una armadura que puede ser equipada por los personajes.
Atributos clave:
- **nombre**: Nombre de la armadura.
- **defensa**: Valor de defensa de la armadura.

#### `Consumible`
Representa un consumible que afecta las estadísticas del personaje (vida o ataque).
Atributos clave:
- **tipo**: Tipo de consumible (Poción de vida, Poción de ataque).
- **potencia**: Cantidad de vida o ataque que proporciona el consumible.

### 🖼 Plantillas y Frontend

- `add_arma.html`: Permite equipar un arma a un personaje.
- `add_armadura.html`: Permite equipar una armadura a un personaje.
- `equipamiento_list.html`: Muestra una lista de todas las armas y armaduras.
- `crear_arma.html`: Formulario para crear un arma nueva.
- `crear_armadura.html`: Formulario para crear una armadura nueva.
- `anadir_item_inventario.html`: Formulario para añadir un item al inventario de un personaje.
# Batalla

Este módulo permite la interacción entre dos personajes seleccionados para una batalla. Los jugadores pueden elegir un personaje y enfrentarse a un personaje controlado por la máquina. La batalla se resuelve mediante turnos, donde cada personaje realiza ataques y recibe daño hasta que uno de ellos pierde toda su vida.

## Funcionalidades

### 1. Selección de personajes
- **Vista `CharacterSelectView`**: Permite a los jugadores seleccionar dos personajes (uno para el jugador y otro para la máquina). Los personajes deben ser diferentes, y se validan antes de proceder a la batalla.
  - **GET**: Muestra un formulario para seleccionar los personajes.
  - **POST**: Procesa los personajes seleccionados y redirige a la batalla.

### 2. Comienzo de la batalla
- **Vista `BattleView`**: Muestra la pantalla de la batalla con los personajes seleccionados y sus ataques disponibles. Cada turno se muestra en la interfaz, junto con los puntos de vida de los personajes.
  - **GET**: Muestra la batalla, con los ataques disponibles de cada personaje.
  - **POST**: Procesa el ataque del jugador, calcula el daño y aplica las consecuencias del turno. Después, la máquina realiza un ataque aleatorio.

### 3. Lógica de la batalla
- **Servicio `BattleService`**: Encargado de gestionar la batalla entre los personajes.
  - **Método `start_battle`**: Inicializa la vida de ambos personajes a 100% al inicio de la batalla.
  - **Método `player_attack`**: Procesa el ataque del jugador, calcula el daño y aplica los efectos de la batalla. Luego, la máquina realiza un ataque aleatorio.
  - **Método `machine_turn`**: La máquina selecciona un ataque aleatorio y realiza su turno.

## Estructura de carpetas y archivos

- **`battle/character_select.html`**: Plantilla para seleccionar los personajes antes de la batalla.
- **`battle/start_battle.html`**: Plantilla que muestra la batalla en curso y los ataques disponibles.
- **`forms.py`**: Contiene el formulario `CharacterSelectionForm` para la selección de personajes.
# Localizaciones
La aplicación **localizaciones** se encarga de la gestión y visualización de las ubicaciones dentro del juego y los personajes asociados a ellas.

### 📌 Funcionalidades principales

- **Visualización de localizaciones**: Los jugadores pueden consultar una lista de las localizaciones predefinidas en el juego a través de la vista `LocalizacionList`.
- **Personajes por localización**: A través de la vista `LocalizacionPersonajes`, los jugadores pueden ver los personajes asociados a una localización específica.
- **Localizaciones predefinidas**: Las localizaciones están preconfiguradas en el juego y no pueden ser creadas ni modificadas manualmente.

### 📂 Modelos principales

#### `Localizacion`
Representa una ubicación dentro del juego. Atributos clave:
- **Nombre** (`nombre`): El nombre único de la localización.
- **Descripción** (`descripcion`): Una descripción detallada de la localización.

Métodos importantes:
- `__str__()`: Devuelve el nombre de la localización para su visualización en el panel de administración y en otros contextos.

### 🤖 API Endpoints

Mediante `LocalizacionViewSet` se exponen los endpoints REST para gestionar localizaciones.

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET | `localizaciones/api/localizaciones/` | Lista todas las localizaciones |
| GET | `localizaciones/api/localizaciones/{id}/` | Obtiene detalles de una localización |

Además, se disponen de vistas adicionales:  

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET | `localizaciones/localizacion_list/` | Renderiza la lista de localizaciones en una vista HTML |
| GET | `localizaciones/localizaciones/{id}/` | Muestra los personajes asociados a una localización específica en una vista HTML |


### 🧐 Vistas

- **`LocalizacionList` (ListView)**: Muestra una lista de todas las localizaciones disponibles en el juego.
- **`LocalizacionPersonajes` (View)**: Permite visualizar los detalles de una localización específica y los personajes asociados a ella.

### 🖼 Plantillas y Frontend

- `localizacion_list.html`: Página que lista todas las localizaciones disponibles en el juego.
- `localizacion_personajes.html`: Página que muestra los detalles de una localización y los personajes asociados a ella.

### 📌 Notas
- Las localizaciones están predefinidas en el juego y no se pueden crear ni modificar desde la app.
- Los personajes están relacionados con las localizaciones, y pueden ser visualizados a través de la vista `LocalizacionPersonajes`.
# Facciones
La aplicación **facciones** gestiona las facciones dentro del juego y sus personajes asociados.

### 📌 Funcionalidades principales

- **Visualización de facciones**: Los jugadores pueden consultar una lista de las facciones disponibles en el juego a través de la vista `FaccionListView`.
- **Personajes por facción**: A través de la vista `FaccionPersonajesView`, los jugadores pueden ver los personajes asociados a una facción específica.
- **Facciones predefinidas**: Las facciones están preconfiguradas en el juego y no pueden ser creadas ni modificadas manualmente.

### 📂 Modelos principales

#### `Faccion`
Representa una facción dentro del juego. Atributos clave:
- **Nombre** (`nombre`): El nombre único de la facción.
- **Descripción** (`descripcion`): Una descripción detallada de la facción, con un valor por defecto de "Sin información conocida".

Métodos importantes:
- `__str__()`: Devuelve el nombre de la facción para su visualización en el panel de administración y en otros contextos.

### 🤖 API Endpoints

Mediante `FaccionViewSet` se exponen los endpoints REST para gestionar facciones.

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET | `facciones/api/facciones/` | Lista todas las facciones |
| GET | `facciones/api/facciones/{id}/` | Obtiene detalles de una facción |

Además, se disponen de vistas adicionales:  

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET | `/faccion_list/` | Renderiza la lista de facciones en una vista HTML |
| GET | `/facciones/{id}/` | Muestra los personajes asociados a una facción específica en una vista HTML |


### 🧐 Vistas

- **`FaccionListView` (ListView)**: Muestra una lista de todas las facciones disponibles en el juego.
- **`FaccionPersonajesView` (DetailView)**: Permite visualizar los detalles de una facción específica y los personajes asociados a ella. Utiliza el contexto `personajes`, que contiene todos los personajes relacionados con esa facción.

### 🖼 Plantillas y Frontend

- `faccion_list.html`: Página que lista todas las facciones disponibles en el juego.
- `faccion_personajes.html`: Página que muestra los detalles de una facción y los personajes asociados a ella.

### 📌 Notas
- Las facciones están predefinidas en el juego y no se pueden crear ni modificar desde la app.
- Los personajes están asociados a las facciones, y pueden ser visualizados a través de la vista `FaccionPersonajesView`.
# `Relacion`
Representa una relación entre dos personajes dentro del juego. Atributos clave:
- **Personaje 1** (`personaje1`): El primer personaje involucrado en la relación.
- **Personaje 2** (`personaje2`): El segundo personaje involucrado en la relación.
- **Tipo de Relación** (`tipo`): El tipo de relación entre los dos personajes. Los valores posibles son:
  - **"A"**: Amigos
  - **"E"**: Enemigos
  - **"N"**: Neutrales

Métodos importantes:
- `get_tipo_display()`: Devuelve el tipo de relación en formato legible, como "Amigos", "Enemigos" o "Neutrales", en lugar de mostrar los códigos (`A`, `E`, `N`).

### 🧐 Vistas

- **`RelacionCreateView` (CreateView)**: Vista que permite crear una nueva relación entre dos personajes en el juego.
- **`RelacionDetailView` (DetailView)**: Muestra los detalles de una relación específica, incluyendo los personajes involucrados y el tipo de relación.

### 🖼 Plantillas y Frontend

- `relacion_form.html`: Página que muestra el formulario para crear una nueva relación entre dos personajes.
- `relacion_detail.html`: Página que muestra los detalles de una relación entre dos personajes, incluyendo su tipo (Amigos, Enemigos, Neutrales).
# TESTING
Para ejecutar los tests en local usar antes:
```bash
python manage.py migrate
```
Los tests están hechos sobre la aplicación Personajes y se dividen en 3 archivos para abarcar los modelos, las urls y las vistas.

### test_models
Valida la funcionalidad de los modelos relacionados con los personajes, inventarios y equipamiento en la aplicación. 
Se incluyen pruebas para la creación de personajes, la gestión de armas y armaduras en el inventario, además de validar el manejo del inventario y los métodos para equipar/desequipar equipamiento.

### test_urls
Valida el correcto funcionamiento de las URLs de la aplicación, tanto para vistas basadas en clases como para la API. Se verifica que las URLs correspondientes a las vistas de personajes (lista, detalles y creación) se resuelvan correctamente y apunten a las vistas y funciones adecuadas. Además me aseguro que las urls de la API de personajes tambíen estén configuradas correctamente

### test_views
valida las vistas asociadas con la creación, detalle y lista de personajes en la aplicación. Se comprueban las siguientes funcionalidades:

- **Vista de detalle de personaje**: Verifica que al acceder a la vista de detalles de un personaje, se muestre la información correcta, se devuelva un código de estado 200 y se use el template adecuado.

- **Vista de creación de personaje**:
  - **GET**: Comprueba que la página de creación cargue correctamente y utilice el template adecuado.
  - **POST**: Verifica que se pueda crear un personaje con datos válidos, que se redirija correctamente y que el personaje se guarde en la base de datos.

- **Vista de lista de personajes**: Asegura que la lista de personajes cargue correctamente, se devuelva un código de estado 200 y se use el template adecuado para la visualización de los personajes.
# Miembros del equipo

- [@Jesús](https://github.com/JesusJimenez01): Encargado de gestionar el grupo, guiar al resto del equipo, estructurar el proyecto, la batalla, los modelos, tests, usar API y la revisión del código
- [@Jorge](https://github.com/jnarjim): Personajes, equipamiento, facciones, localizaciones y tests
- [@Estefany](https://github.com/estefany89): Relaciones, Inicio

>[!NOTE]
>Tuve que subir algunas cosas por mi cuenta por temas relacionados con las ramas y en Insights sale un poco desbalanceado pero el proyecto se ha repartido práctimante 50% Jesús y 50% Jorge, Estefany lo ha intentado 👍
