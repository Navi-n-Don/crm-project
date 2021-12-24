from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class Person(AbstractUser, models.Model):
    image = models.ImageField(upload_to='users', default='default.png')

    class Meta:
        ordering = ('username', '-date_joined',)
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        """
        String for representing a Person object.
        """
        return self.username
