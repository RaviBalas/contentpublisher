from django.db import models
from common.models import Audit
from social_media.models import Credentials, Category


class StatusChoices(models.TextChoices):
    CREATED = "created"
    PUBLIC_URL_CREATED = "public_url_created"
    SUCCESS = "success"
    FAILED = "failed"


class MediaChoices(models.TextChoices):
    REELS = "reels"
    SHORTS = "shorts"
    VIDEO = "video"


class ContentModel(Audit):
    category = models.ForeignKey(Category, related_name="contents", on_delete=models.SET_NULL, null=True)
    source_identifier = models.ForeignKey(Credentials, on_delete=models.CASCADE, related_name="source_contents")
    social_media_url = models.TextField(unique=True, null=True, blank=True)
    social_media_type = models.CharField(max_length=10, choices=MediaChoices.choices, null=True, blank=True)
    media_public_url = models.TextField(null=True, blank=True)
    media_name = models.CharField(max_length=255, null=True, blank=True)
    intermediate_id = models.CharField(max_length=255, null=True, blank=True)
    destination_identifier = models.ForeignKey(Credentials, on_delete=models.CASCADE,
                                               related_name="destination_contents")
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.CREATED)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.source_identifier} >> {self.destination_identifier} = {self.status}"
