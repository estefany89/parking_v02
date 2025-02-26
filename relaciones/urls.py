from django.urls import path

from batalla.urls import app_name
from .views import RelacionListView, RelacionDetailView, RelacionCreateView, RelacionUpdateView, RelacionDeleteView

app_name = 'relaciones'
urlpatterns = [
    path('relaciones/', RelacionListView.as_view(), name='relacion_list'),
    path('relaciones/<int:pk>/', RelacionDetailView.as_view(), name='relacion_detail'),
    path('relaciones/nueva/', RelacionCreateView.as_view(), name='relacion_create'),
    path('relaciones/<int:pk>/editar/', RelacionUpdateView.as_view(), name='relacion_update'),
    path('relaciones/<int:pk>/eliminar/', RelacionDeleteView.as_view(), name='relacion_delete'),
]