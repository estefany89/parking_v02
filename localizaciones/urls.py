from django.urls import path
from .views import LocalizacionList, LocalizacionPersonajes

app_name = 'localizaciones'

urlpatterns = [
    path('localizacion_list', LocalizacionList.as_view(), name='localizacion_list'),
    path('<int:pk>/', LocalizacionPersonajes.as_view(), name='localizacion_personajes'),
]