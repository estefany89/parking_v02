from django.urls import path
from .views import CharacterSelectView, BattleView

app_name = 'battle'

urlpatterns = [
    path('select/', CharacterSelectView.as_view(), name='character_select'),

    path('start/<int:player_id>/<int:machine_id>/', BattleView.as_view(), name='start_battle'),
]
