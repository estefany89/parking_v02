from django import forms
from personajes.models import Personaje

class CharacterSelectionForm(forms.Form):
    player_character = forms.ModelChoiceField(queryset=Personaje.objects.all(), label='Player Character')
    machine_character = forms.ModelChoiceField(queryset=Personaje.objects.all(), label='Machine Character')
