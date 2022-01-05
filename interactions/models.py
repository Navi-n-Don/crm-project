from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse_lazy
from main import settings
from main.constants import APPEALS
from someapp.models import Project


class Interaction(models.Model):
    """
    Model representing a interactions between company and manager
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    appeals = models.CharField(max_length=2, choices=APPEALS.choices, default=APPEALS.REQUEST)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = RichTextField(config_name='comment_ckeditor')
    rating = models.ForeignKey('Star', on_delete=models.CASCADE)
    keyword = models.ManyToManyField('Keyword', related_name='keyword')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model metadata of interaction
        """
        ordering = ('-created_date', '-rating',)
        verbose_name = 'interaction'
        verbose_name_plural = 'interactions'

    def __str__(self) -> str:
        """
        String for representing a interaction object.
        """
        return self.get_appeals()

    def get_absolute_url(self) -> str:
        """
        Canonical URL for an object
        """
        return reverse_lazy('interaction-details', args=[str(self.id)])

    def get_appeals(self):
        return f'{APPEALS(self.appeals).label}'


class Keyword(models.Model):
    """
    Model representing a keyword
    """
    title = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model metadata of keyword
        """
        ordering = ('-created_date',)
        verbose_name = 'keyword'
        verbose_name_plural = 'keywords'

    def __str__(self) -> str:
        """
        String for representing a keyword object.
        """
        return f'{self.title}'


class Star(models.Model):
    """
    Model representing a star for rating
    """
    value = models.SmallIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model metadata of star
        """
        ordering = ('-value',)
        verbose_name = 'star'
        verbose_name_plural = 'stars'

    def __str__(self) -> str:
        """
        String for representing a star object.
        """
        return f'{self.value}'
