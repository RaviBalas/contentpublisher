from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import PlatformInfo, Credentials


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
