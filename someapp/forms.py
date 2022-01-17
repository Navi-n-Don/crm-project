from django import forms
from django.forms import inlineformset_factory
from .models import Company, Email, Phone, Project


class CompanyForm(forms.ModelForm):
    """Form for create or update company objects"""
    class Meta:
        model = Company
        fields = ('title', 'contact_person', 'description', 'address',)


PhoneInlineFormSet = inlineformset_factory(
    Company, Phone, fields=('phone_number',), extra=1, max_num=5, can_delete=True)
EmailInlineFormSet = inlineformset_factory(
    Company, Email, fields=('email_address',), extra=1, max_num=5, can_delete=True)


class DateInput(forms.DateInput):
    """Assignment to a field of type date
    Attributes:
        input_type (str): specifies the type of the assigned field
    """
    input_type = 'date'


class ProjectForm(forms.ModelForm):
    """Form for create a new project objects"""
    class Meta:
        model = Project
        fields = ('title', 'company', 'description', 'creator', 'begin', 'end', 'price',)
        widgets = {
            'begin': DateInput(),
            'end': DateInput(),
        }


class ProjectUpdateForm(forms.ModelForm):
    """Form for update the project objects"""
    class Meta:
        model = Project
        exclude = ('company', 'creator', 'today_date', )
        widgets = {
            'begin': DateInput(),
            'end': DateInput(),
        }
