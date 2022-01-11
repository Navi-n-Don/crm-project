import django_filters
from django import forms
from interactions.models import Interaction, Keyword
from main.constants import PROJECT_ORDERING, COMPANY_ORDERING
from someapp.models import Company, Project


class CompanyFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('created_date', 'created_date'),
        ),
        choices=COMPANY_ORDERING,
        empty_label=None
    )

    class Meta:
        model = Company
        fields = ['title', 'created_date']


class ProjectFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('begin', 'begin'),
            ('end', 'end'),
        ),
        choices=PROJECT_ORDERING,
        empty_label=None
    )

    class Meta:
        model = Project
        fields = ['title', 'begin', 'end', ]


class Filter(django_filters.FilterSet):
    keyword = django_filters.ModelMultipleChoiceFilter(
        field_name='keyword__title',
        to_field_name='title',
        widget=forms.CheckboxSelectMultiple,
        label='Keywords',
        queryset=Keyword.objects.all()
    )

    class Meta:
        model = Interaction
        fields = ['keyword', ]