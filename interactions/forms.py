from django import forms
from interactions.models import Interaction


class ActionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ('appeals', 'description',)


class ActionUpdateForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ('appeals', 'description', 'rating',)
