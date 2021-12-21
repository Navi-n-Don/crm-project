from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Person


class PersonCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Person
        fields = ('username', 'email')


class PersonChangeForm(UserChangeForm):
    class Meta:
        model = Person
        fields = ('username', 'email')
