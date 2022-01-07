import django_filters
from interactions.models import Interaction
from main.constants import APPEALS_ORDERING, PROJECT_ORDERING, COMPANY_ORDERING
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


class ActionFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('appeals', 'appeals'),
            ('created_date', 'created_date'),
        ),
        choices=APPEALS_ORDERING,
        empty_label=None
    )

    class Meta:
        model = Interaction
        fields = ['appeals', 'created_date', ]
