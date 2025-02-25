from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocalizacionPersonajes, lista_localizaciones, LocalizacionViewSet

router = DefaultRouter()
router.register(r'localizaciones', LocalizacionViewSet)

app_name = 'localizaciones'

urlpatterns = [
    path('localizacion_list', lista_localizaciones, name='localizacion_list'),
    path('<int:pk>/', LocalizacionPersonajes.as_view(), name='localizacion_personajes'),
    path('api/', include(router.urls)),
]