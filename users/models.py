from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser):
    """
    Model representing a person
    """
    image = models.ImageField(upload_to='users', default='default.png')

    class Meta:
        """
        Model metadata of person
        """
        ordering = ('username', '-date_joined',)
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self) -> str:
        """
        String for representing a Person object.
        """
        return f'{self.username}'
