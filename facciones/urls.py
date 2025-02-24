from django.urls import path

from batalla.urls import app_name
from . import views

app_name = "facciones"
urlpatterns = [
    path('', views.lista_facciones, name='lista_facciones'),
]