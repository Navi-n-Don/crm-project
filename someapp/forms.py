from django import forms
from django.forms import inlineformset_factory
from .models import Company, Email, Phone


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('contact_person', 'description', 'address', 'created_date', 'updated_date',)


PhoneInlineFormSet = inlineformset_factory(Company, Phone, fields=('phone_number',))
EmailInlineFormSet = inlineformset_factory(Company, Email, fields=('email_address',))
