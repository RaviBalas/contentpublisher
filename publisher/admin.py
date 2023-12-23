from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ContentModel, StatusChoices


@admin.register(ContentModel)
class ContentModelAdmin(ImportExportModelAdmin):
    list_display = ("created_at", "media_name", "category", "updated_at", "status", "source_identifier",
                    "social_media_url", "media_public_url", "intermediate_id", "destination_identifier", "error")
    search_fields = ("media_name", "media_name", "social_media_url", "media_public_url")
    list_filter = ("status", "category", "source_identifier", "destination_identifier", 'created_at')
    ordering = ("-created_at",)
    list_per_page = 25

    actions = ['mark_created', 'mark_public_url_created']

    def mark_created(self, request, queryset):
        for i in queryset:
            i.status = StatusChoices.CREATED
            i.save()

    mark_created.short_description = "Mark select contents as created"

    def mark_public_url_created(self, request, queryset):
        for i in queryset:
            i.status = StatusChoices.PUBLIC_URL_CREATED
            i.save()

    mark_public_url_created.short_description = "Mark select contents as PUBLIC URL CREATED"
