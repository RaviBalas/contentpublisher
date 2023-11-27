from django.db import models
from common.models import Audit
from social_media.models import Credentials


class ContentModel(Audit):
    source_identifier = models.ForeignKey(Credentials, on_delete=models.CASCADE, related_name="source_contents")
    social_media_url = models.TextField(null=True, blank=True)
    video_public_url = models.TextField(null=True, blank=True)
    intermediate_id = models.CharField(max_length=255, null=True, blank=True)
    destination_identifier = models.ForeignKey(Credentials, on_delete=models.CASCADE,
                                               related_name="destination_contents")
    status = models.CharField(max_length=50, default="CREATED")
    error = models.CharField(max_length=20, null=True, blank=True)
