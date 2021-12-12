from django.contrib import admin
from .models import Company, Phone, Email, Project


# Register your models here.
class PhoneInline(admin.TabularInline):
    model = Phone
    fields = ('phone_number',)
    can_delete = False
    extra = 1
    max_num = 5


class EmailInline(admin.TabularInline):
    model = Email
    fields = ('email_address',)
    can_delete = False
    extra = 1
    max_num = 5


class ProjectInline(admin.TabularInline):
    model = Project
    fields = ('title', 'slug', 'description', 'price', 'begin', 'end',)
    can_delete = False
    extra = 1


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'company',)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'company',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description', 'price', 'begin', 'end',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'contact_person', 'description', 'address', 'created_date', 'updated_date',)
    inlines = [PhoneInline, EmailInline, ProjectInline]
