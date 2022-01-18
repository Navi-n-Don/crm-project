from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from main.utils import valid_username, update_to


class Person(AbstractUser):
    """Model representing a person"""
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, and digits only.",
        validators=[valid_username],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    image = models.ImageField(upload_to=update_to,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg'])],
                              default='default.png')

    class Meta:
        ordering = ('username', '-date_joined',)
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self) -> str:
        """String for representing a Person object."""
        return f'{self.username}'

    def save(self, *args, **kwargs) -> None:
        """Custom save new image method
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        try:
            this = Person.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)
