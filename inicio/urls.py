from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
app_name = 'inicio'

urlpatterns = [
    path('', views.mostrar_menu, name='mostrar_menu'),  # <-- Cambia aquí
]