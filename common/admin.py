from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ApiLogsModel, CustomLog


@admin.register(ApiLogsModel)
class ApiLogsModelAdmin(ImportExportModelAdmin):
    list_display = ("created_at", "task_name", "status_code", "request_type", "url", "error", "param", "data", "files",
                    "json", "response", "time_taken")
    ordering = ("-created_at",)
    search_fields = ("type", "url", "task_name")
    list_filter = ("task_name", "status_code", "request_type")
    list_per_page = 25


@admin.register(CustomLog)
class CustomLogAdmin(ImportExportModelAdmin):
    list_display = ("created_at", "level", "msg", "trace", "create_datetime", "error", "method")
    search_fields = ("error", "msg")
    list_filter = ("level",)
    ordering = ("-created_at",)
    list_per_page = 25
