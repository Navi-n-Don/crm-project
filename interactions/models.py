from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse_lazy
from main import settings
from main.constants import APPEALS
from someapp.models import Project, Company


class Interaction(models.Model):
    """Model representing a interactions between company and manager"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    appeals = models.CharField(max_length=2, choices=APPEALS.choices, default=APPEALS.REQUEST)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = RichTextField(config_name='comment_ckeditor')
    keyword = models.ManyToManyField('Keyword', related_name='keyword', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'interaction'
        verbose_name_plural = 'interactions'

    def __str__(self) -> str:
        """String for representing a interaction object."""
        return self.get_appeals()

    def get_appeals(self) -> str:
        """Method to get a value of appeals"""
        return f'{APPEALS(self.appeals).label}'


class Keyword(models.Model):
    """Model representing a keyword"""
    title = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'keyword'
        verbose_name_plural = 'keywords'

    def __str__(self) -> str:
        """String for representing a keyword object."""
        return f'{self.title}'


class Like(models.Model):
    """Model representing a Like"""
    who = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.ForeignKey(Interaction, on_delete=models.CASCADE)
    like = models.ForeignKey("Rating", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'like'
        verbose_name_plural = 'likes'

    def __str__(self) -> str:
        """String for representing the CommentLike object."""
        return f'{self.action} - {self.who}'


class Rating(models.Model):
    """Model representing a Rating"""
    value = models.SmallIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-value',)
        verbose_name = 'rating'
        verbose_name_plural = 'rating'

    def __str__(self) -> str:
        """String for representing a Rating object."""
        return f'{self.value}'
