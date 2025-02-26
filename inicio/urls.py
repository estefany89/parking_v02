from django.urls import path

from batalla.urls import app_name
from . import views
app_name = 'inicio'

urlpatterns = [
    path('inicio/', views.mostrar_menu, name='mostrar_menu'),
]