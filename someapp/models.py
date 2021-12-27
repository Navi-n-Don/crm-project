from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from slugify import slugify
from main import settings
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
        """
        Model metadata of company
        """
        ordering = ('title', 'created_date',)
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self) -> str:
        """
        String for representing the Client object.
        """
        return f'{self.title}'

    def save(self, *args, **kwargs) -> None:
        """
        Filling in the slug field
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Company, self).save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """
        Canonical URL for an object
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
        """
        Model metadata of phone number
        """
        ordering = ('company',)
        verbose_name = 'phone number'
        verbose_name_plural = 'phone numbers'

    def __str__(self) -> str:
        """
        String for representing a phone number object.
        """
        return f'{self.phone_number}'


class Email(models.Model):
    """
    Model representing a e-mail address
    """
    email_address = models.EmailField(max_length=250, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model metadata of e-mail address
        """
        ordering = ('company',)
        verbose_name = 'email address'
        verbose_name_plural = 'email addresses'

    def __str__(self) -> str:
        """
        String for representing a email address object.
        """
        return f'{self.email_address}'


class Project(models.Model):
    """
    Model representing a project
    """
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField()
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, default='', null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="responsible",
                                default='', null=True)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    begin = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    today_date = datetime.date.today()

    class Meta:
        """
        Model metadata of a project
        """
        ordering = ('title',)
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def save(self, *args, **kwargs) -> None:
        """
        Filling in the slug field
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self) -> str:
        """
        String for representing a project object.
        """
        return f'{self.title}'

    def get_absolute_url(self) -> str:
        """
        Canonical URL for an object
        """
        return reverse('project-details', kwargs={'company_slug': slugify(str(self.company)), 'project_slug': self.slug})

    @property
    def days_to(self) -> list:
        """
        Сalculation of the project status for today
        """
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
