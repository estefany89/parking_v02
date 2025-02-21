from django import forms
from django.forms import inlineformset_factory
from .models import Arma, Ataque


class ArmaForm(forms.ModelForm):
    class Meta:
        model = Arma
        fields = ['nombre', 'dano_base', 'tipo', 'es_unica']

class AtaqueForm(forms.ModelForm):
    class Meta:
        model = Ataque
        fields = ['nombre', 'dano']

# InlineFormSet para asegurar entre 1 y 4 ataques
AtaqueFormSet = inlineformset_factory(
    Arma, Ataque,
    form=AtaqueForm,
    extra=3,
    min_num=1,  # Mínimo 1 ataque
    max_num=4,  # Máximo 4 ataques
    validate_min=True,
    validate_max=True
)