# Generated by Django 3.2.9 on 2021-12-25 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('someapp', '0004_auto_20211225_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='keyword',
            field=models.ManyToManyField(related_name='keyword', to='someapp.Keyword'),
        ),
    ]
