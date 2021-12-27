from django.contrib import admin
from interactions.models import Interaction, Star


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'updated_date',)
    list_display = ('appeals', 'description', 'manager', 'project', 'rating',)
    fieldsets = (
        ('General', {
            'fields': ('appeals', 'description', 'keyword', 'rating',)
        }),
        ('Project', {
            'fields': ('project',)
        }),
        ('Responsible', {
            'fields': ('manager',)
        }),
        ('Other', {
            'fields': ('created_date', 'updated_date',)
        }),
    )


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'updated_date',)
    list_display = ('value',)
