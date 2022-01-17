from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Person


class PersonCreationForm(UserCreationForm):
    """Form for create a new person objects"""
    class Meta(UserCreationForm):
        model = Person
        fields = ('username', 'email')


class PersonChangeForm(UserChangeForm):
    """Form for change data person objects"""
    class Meta:
        model = Person
        fields = ('username', 'email')


class PersonUpdateForm(forms.ModelForm):
    """Form for update person objects"""
    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'email', 'image',)
