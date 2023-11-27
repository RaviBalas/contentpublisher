from celery import shared_task

from .models import ContentModel
from social_media.accounts import AccountManager
import logging

logger = logging.getLogger("db")


@shared_task(name="generate_public_url", queue="main_queue")
def generate_public_url(source_identifier=None, content_ids=None):
    logger.log(level=10, msg=f"in generate public url {source_identifier}, {content_ids}")
    if content_ids is None:
        content_ids = []
    if content_ids:
        content_queryset = ContentModel.objects.filter(id__in=content_ids)
    elif source_identifier:
        content_queryset = ContentModel.objects.filter(source_identifier__identifier=source_identifier)
    else:
        content_queryset = ContentModel.objects.filter(video_public_url=None)

    for inst in content_queryset:
        account_obj = AccountManager(inst.source_identifier.platform.name).account_obj
        res, is_success = account_obj.generate_public_url(inst.social_media_url)
        if is_success:
            inst.video_public_url = res.get("url")
            inst.status = "PUBLIC_URL_CREATED"
        else:
            inst.error = res
            inst.status = "FAILED"
        inst.save(update_fields=["updated_at", "video_public_url", "status", "error"])


@shared_task(name="publish_content", queue="main_queue")
def publish_content(destination_identifier=None, content_ids=None):
    logger.log(level=10, msg=f"in  publish content: {destination_identifier}, {content_ids}")
    if content_ids is None:
        content_ids = []
    if content_ids:
        content_queryset = ContentModel.objects.filter(id__in=content_ids)
    elif destination_identifier:
        content_queryset = ContentModel.objects.filter(destination_identifier__identifier=destination_identifier)
    else:
        content_queryset = ContentModel.objects.filter(status="PUBLIC_URL_CREATED")

    for inst in content_queryset:
        account_obj = AccountManager(inst.destination_identifier.platform.name).account_obj
        res, is_success = account_obj.publish_content(inst.social_media_url)
        if is_success:
            inst.status = "SUCCESS"
            inst.error = None
        else:
            inst.error = res
            inst.status = "FAILED"
        inst.save(update_fields=["updated_at", "status", "error"])
