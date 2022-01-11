from django import forms
from interactions.models import Interaction, Like, Rating, Keyword


class ActionForm(forms.ModelForm):
    keyword = forms.ModelMultipleChoiceField(
            queryset=Keyword.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)

    class Meta:
        model = Interaction
        fields = ('appeals', 'description', 'keyword',)


class LikeForm(forms.ModelForm):
    like = forms.ModelChoiceField(queryset=Rating.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Like
        fields = ('like',)


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('title',)
