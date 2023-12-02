import logging
from celery import shared_task
from .models import ContentModel, StatusChoices
from social_media.accounts import AccountManager

logger = logging.getLogger("db")


@shared_task(name="content_creator", queue="main_queue")
def content_creator(category, source_identifier, dest_identifier):
    acc_obj = AccountManager("account")
    source_identi_obj = acc_obj.get_account_object.get_credential_using_identifier(source_identifier)
    dest_identi_obj = acc_obj.get_account_object.get_credential_using_identifier(dest_identifier)
    account_obj = AccountManager(source_identi_obj.platform.name).account_obj
    category_obj = account_obj.get_category_obj(category)
    listing = account_obj.list_of_social_media_listing(category, source_identifier)

    for obj in listing:
        ContentModel.objects.update_or_create(social_media_url=obj["url"], defaults={
            "destination_identifier": dest_identi_obj, "source_identifier": source_identi_obj,
            "category": category_obj})
    return listing


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
            inst.media_public_url = res.get("url")
            inst.media_name = res.get("name")
            inst.status = StatusChoices.PUBLIC_URL_CREATED
            inst.error = None
        else:
            inst.error = res
            inst.status = StatusChoices.FAILED
        inst.save(update_fields=["updated_at", "media_public_url", "media_name", "status", "error"])


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
        res, is_success = account_obj.publish_content(inst.destination_identifier.identifier,
                                                      media_caption=inst.media_name, media_url=inst.media_public_url)
        if is_success:
            inst.status = StatusChoices.SUCCESS
            inst.error = None
        else:
            inst.error = res
            inst.status = StatusChoices.FAILED
        inst.save(update_fields=["updated_at", "status", "error"])
