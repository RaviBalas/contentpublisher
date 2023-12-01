from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContentModel, StatusChoices
from .tasks import generate_public_url, publish_content


@receiver(post_save, sender=ContentModel)
def send_for_video_download(sender, instance, created, **kwargs):
    if created or instance.status == StatusChoices.CREATED:
        generate_public_url.delay(content_ids=[instance.id, ])
    elif instance.status == StatusChoices.PUBLIC_URL_CREATED:
        publish_content.delay(content_ids=[instance.id, ])
