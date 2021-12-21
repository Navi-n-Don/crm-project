from django import forms
from django.forms import inlineformset_factory
from .models import Company, Email, Phone, Project


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('title', 'contact_person', 'description', 'address',)


PhoneInlineFormSet = inlineformset_factory(Company, Phone, fields=('phone_number',), extra=1, max_num=5)
EmailInlineFormSet = inlineformset_factory(Company, Email, fields=('email_address',), extra=1, max_num=5)

