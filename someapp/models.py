from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class Company(models.Model):
    """
    Model representing a company
    """
    title = models.CharField(max_length=250, help_text="Enter a name of company", unique=True)
    slug = models.SlugField(max_length=250, help_text="Enter a slug-name of company", unique=True)
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

    def get_absolute_url(self):
        """
        Returns the url to access a particular record.
        """
        return reverse('company-details', kwargs={'slug': self.slug})


class Phone(models.Model):
    """
    Model representing a phone number
    """
    phone_number = models.CharField(max_length=130, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number


class Email(models.Model):
    """
    Model representing a e-mail address
    """
    email_address = models.CharField(max_length=250, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.email_address


class Project(models.Model):
    """
    Model representing a project
    """
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    begin = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def get_absolute_url(self):
        return reverse('project-details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
