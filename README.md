# PARKING INTELIGENTE


## 🛠 Installación y configuración del proyecto

Para poder probar el proyecto correctamente sigue los siguientes pasos:

1. Construir y levantar los contenedores
```bash
docker compose up --build -d
```
1. Aplicar migraciones y cargar datos
```bash
docker compose exec web python manage.py migrate
```
1. Crear un superusuario para poder acceder al admin en caso de querer comprobarlo
```bash
docker compose exec web python manage.py createsuperuser
```
1. Acceder a la aplicación
http://localhost:8000/inicio
    
