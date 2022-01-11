from django.contrib import admin
from interactions.models import Interaction, Rating, Like, Keyword


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'updated_date',)
    list_display = ('appeals', 'description', 'manager', 'project',)
    fieldsets = (
        ('General', {
            'fields': ('appeals', 'description', 'keyword',)
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


@admin.register(Like)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['who', 'action', 'like', ]
    readonly_fields = ('created_date', 'updated_date',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['value', ]
    readonly_fields = ('created_date', 'updated_date',)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    readonly_fields = ('created_date', 'updated_date',)
