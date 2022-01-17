from django import forms
from interactions.models import Interaction, Like, Rating, Keyword


class ActionForm(forms.ModelForm):
    """Form for create or update interaction objects"""
    keyword = forms.ModelMultipleChoiceField(
            queryset=Keyword.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)

    class Meta:
        model = Interaction
        fields = ('appeals', 'description', 'keyword',)


class LikeForm(forms.ModelForm):
    """Form for adding likes to interaction"""
    like = forms.ModelChoiceField(queryset=Rating.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Like
        fields = ('like',)


class KeywordForm(forms.ModelForm):
    """Form for create a new keyword object"""
    class Meta:
        model = Keyword
        fields = ('title',)
