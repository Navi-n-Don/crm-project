from django import forms
from interactions.models import Interaction, Like, Rating


class ActionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ('appeals', 'description',)


class ActionUpdateForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ('appeals', 'description',)


class LikeForm(forms.ModelForm):
    like = forms.ModelChoiceField(queryset=Rating.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Like
        fields = ('like',)
