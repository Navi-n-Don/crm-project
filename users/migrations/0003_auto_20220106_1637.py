# Generated by Django 3.2.9 on 2022-01-06 14:37

from django.db import migrations, models
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_person_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(default='default.png', upload_to=main.utils.update_to),
        ),
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, and digits only.', max_length=150, unique=True, validators=[main.utils.valid_username]),
        ),
    ]
