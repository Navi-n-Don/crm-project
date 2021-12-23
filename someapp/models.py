from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from slugify import slugify
from main import settings
from someapp.choices import APPEALS
import datetime


# Create your models here.
class Company(models.Model):
    """
    Model representing a company
    """
    title = models.CharField(max_length=250, help_text="Enter a name of company", unique=True)
    slug = models.SlugField()
    contact_person = models.CharField(max_length=250, help_text="Enter a name of the head of the company")
    description = RichTextField()
    address = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title', 'created_date',)
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        """
        String for representing the Client object.
        """
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Company, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Returns the url to access a particular record.
        """
        return reverse('company-details', kwargs={'slug': self.slug})


class Phone(models.Model):
    """
    Model representing a phone number
    """
    valid_re = RegexValidator(regex=r"\d{3}-\d{7}",
                              message="Phone number must be entered in the format: '000-0000000'. Up to 11 digits "
                                      "allowed.")
    phone_number = models.CharField(validators=[valid_re], max_length=11, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('company',)
        verbose_name = 'phone number'
        verbose_name_plural = 'phone numbers'

    def __str__(self):
        return self.phone_number


def validate_email(value):
    """
    Validate that a username is email like.
    """
    _validate_email = EmailValidator()

    try:
        _validate_email(value)
    except ValidationError:
        raise ValidationError(_('Enter a valid email address.'))

    return value


class Email(models.Model):
    """
    Model representing a e-mail address
    """
    email_address = models.CharField(validators=[validate_email], max_length=250, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('company',)
        verbose_name = 'email address'
        verbose_name_plural = 'email addresses'

    def __str__(self):
        return self.email_address


class Project(models.Model):
    """
    Model representing a project
    """
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField()
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default='')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="responsible",
                                default='')
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    begin = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    today_date = datetime.date.today()

    class Meta:
        ordering = ('title',)
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-details', kwargs={'company_slug': slugify(str(self.company)), 'project_slug': self.slug})

    @property
    def days_to(self):
        date_diff_start = (self.begin - self.today_date).days
        date_diff_end = (self.end - self.today_date).days
        if (date_diff_start >= 0) and (date_diff_start < 4):
            return [f'left {date_diff_start} day', 'text-secondary']
        elif date_diff_start >= 4:
            return [f'left {date_diff_start} days', 'text-secondary']
        elif (date_diff_start < 0) and (date_diff_end >= 0):
            return ['In Progress', 'text-info']
        elif (date_diff_start < 0) and (date_diff_end < 0):
            return ['Completed', 'text-success']


class Interaction(models.Model):
    """
    Model representing a interactions between company and manager
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    appeals = models.CharField(max_length=20, choices=APPEALS, default='')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = RichTextField()
    rating = models.SmallIntegerField(validators=[MinValueValidator(-5), MaxValueValidator(5)])
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_date', '-rating',)
        verbose_name = 'interaction'
        verbose_name_plural = 'interactions'

    def __str__(self):
        return self.project

    def get_absolute_url(self):
        return reverse('interaction-details', args=[str(self.id)])
