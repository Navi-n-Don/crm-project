from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Person


class PersonCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Person
        fields = ('username', 'email')


class PersonChangeForm(UserChangeForm):
    class Meta:
        model = Person
        fields = ('username', 'email')


class PersonUpdateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'email', 'image',)
