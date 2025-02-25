from django.urls import path
from .views import FaccionListView, FaccionPersonajesView

app_name = 'facciones'

urlpatterns = [
    path('faccion_list', FaccionListView.as_view(), name='faccion_list'),
    path('<int:pk>/', FaccionPersonajesView.as_view(), name='faccion_personajes'),
]
