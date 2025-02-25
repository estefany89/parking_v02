from django.urls import path, include
from .views import FaccionPersonajesView, FaccionViewSet, lista_facciones
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'facciones', FaccionViewSet)

app_name = 'facciones'

urlpatterns = [
    path('api/', include(router.urls)),
    path('faccion_list', lista_facciones, name='faccion_list'),
    path('<int:pk>/', FaccionPersonajesView.as_view(), name='faccion_personajes'),
]
