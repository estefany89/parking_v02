from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.mostrar_menu, name='mostrar_menu'),
]