from django.forms import ModelForm
from django.forms.models import inlineformset_factory

import models


class TeamForm(ModelForm):
    error_css_class = 'text-error'
    required_css_class = 'text-required'

    class Meta:
        model = models.Team


class PlayerForm(ModelForm):
    error_css_class = 'text-error'
    required_css_class = 'text-required'

    class Meta:
        model = models.Player


class GameForm(ModelForm):
    error_css_class = 'text-error'
    required_css_class = 'text-required'

    class Meta:
        model = models.Game
        fields = ('played_on', 'location', )


TeamPlayerFormSet = inlineformset_factory(models.Team, models.Player)
