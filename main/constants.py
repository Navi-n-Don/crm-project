from django.db import models

COMPANY_ORDERING = [
    ('title', 'ascending (company name)'),
    ('-title', 'descending (company name)'),
    ('created_date', 'ascending (creation date)'),
    ('-created_date', 'descending (creation date)'),
]

PROJECT_ORDERING = [
    ('title', 'A-Z'),
    ('-title', 'Z-A'),
    ('begin', '1-9 Date Begin'),
    ('-begin', '9-1 Date Begin'),
    ('end', '1-9 Date End'),
    ('-end', '9-1 Date End'),
]


class APPEALS(models.TextChoices):
    REQUEST = 'RQ', 'Request'
    LETTER = 'LT', 'Letter'
    WEBSITE = 'WS', 'Website'
    COMPANY = 'CO', 'Company Initiative'
