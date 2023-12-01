from django.db import models
from common.models import Audit
from social_media.models import Credentials, Category


class StatusChoices(models.TextChoices):
    CREATED = "created"
    PUBLIC_URL_CREATED = "public_url_created"
    SUCCESS = "success"
    FAILED = "failed"


class ContentModel(Audit):
    category = models.ForeignKey(Category, related_name="contents", on_delete=models.SET_NULL, null=True)
    source_identifier = models.ForeignKey(Credentials, on_delete=models.CASCADE, related_name="source_contents")
    social_media_url = models.TextField(null=True, blank=True)
    media_public_url = models.TextField(null=True, blank=True)
    media_name = models.CharField(max_length=255, null=True, blank=True)
    intermediate_id = models.CharField(max_length=255, null=True, blank=True)
    destination_identifier = models.ForeignKey(Credentials, on_delete=models.CASCADE,
                                               related_name="destination_contents")
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.CREATED)
    error = models.TextField(null=True, blank=True)
