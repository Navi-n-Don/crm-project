from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import PersonCreationForm, PersonChangeForm
from .models import Person
from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "d E Y (H:i:s)"


class PersonAdmin(UserAdmin):
    add_form = PersonCreationForm
    form = PersonChangeForm
    model = Person
    list_display = ['username', 'email', 'is_staff', 'date_joined', ]
    readonly_fields = ('last_login', 'date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Image', {
            'fields': ('image',)
        }),
    )


admin.site.register(Person, PersonAdmin)