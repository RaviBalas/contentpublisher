from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ContentModel


@admin.register(ContentModel)
class ContentModelAdmin(ImportExportModelAdmin):
    list_display = (
        "created_at", "updated_at", "status", "source_identifier", "social_media_url", "video_public_url",
        "intermediate_id", "destination_identifier", "error")
    search_fields = ('source_identifier__platform__name',)
    list_filter = ("status",)
    list_per_page = 25
