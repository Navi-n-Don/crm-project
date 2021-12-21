import django_filters
from .models import Company, Project


class CompanyFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('created_date', 'created_date'),
        ),
        choices=[
            ('title', 'ascending (company name)'),
            ('-title', 'descending (company name)'),
            ('created_date', 'ascending (creation date)'),
            ('-created_date', 'descending (creation date)'),
        ],
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
        choices=[
            ('title', 'A-Z'),
            ('-title', 'Z-A'),
            ('begin', '1-9 Date Begin'),
            ('-begin', '9-1 Date Begin'),
            ('end', '1-9 Date End'),
            ('-end', '9-1 Date End'),
        ],
        empty_label=None
    )

    class Meta:
        model = Project
        fields = ['title', 'begin', 'end', ]