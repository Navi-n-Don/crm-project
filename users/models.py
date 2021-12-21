from django.contrib.auth.models import AbstractUser
from django.db import models


class Person(AbstractUser, models.Model):
    image = models.ImageField(upload_to='users', default='default.png')
