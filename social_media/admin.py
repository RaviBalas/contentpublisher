from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import PlatformInfo, Credentials, Tags, Category


@admin.register(Tags)
class TagsAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ('name',)
    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ('name',)
    filter_horizontal = ("tags",)
    list_per_page = 25


@admin.register(PlatformInfo)
class PlatformInfoAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ('file__main_doc__proposal__number',)
    list_per_page = 25


@admin.register(Credentials)
class CredModelAdmin(ImportExportModelAdmin):
    list_display = ("platform", "identifier", "client_id", "client_secret", "api_key", "username", "password")
    search_fields = ('platform',)
    list_per_page = 25
