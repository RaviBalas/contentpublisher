import logging
import time
import posixpath
import urllib.parse

from django.conf import settings

from common.utils import req_api_wrapper
from social_media.models import Credentials
from .account import Account
from social_media.initial_mapping import instagram_error_keys_codes

logger = logging.getLogger("db")


class Instagram(Account):
    def __init__(self, *args, **kwargs):
        self.name = "instagram"
        self.base_url = settings.FACEBOOK_ENDPOINT
        super(Instagram, self).__init__(*args, **kwargs)
        self.error_code_mapping = instagram_error_keys_codes

    def list_of_social_media_listing(self, category, identifier, **kwargs):
        return []

    def generate_public_url(self, social_media_url):
        pass  # return public_url

    def get_list_of_media(self, identifier):
        obj = Credentials.objects.get(platform__name=self.name, identifier=identifier)
        url = posixpath.join(self.base_url, obj.extra_conf['ig_user_id'], "media")
        params = {"access_token": obj.access_token}  # user_access_token
        res, is_success = req_api_wrapper("GET", url, params=params, task_name="list_of_media_in_IG")
        return res, is_success

    def create_container(self, identifier, video_url, video_caption="no caption!!"):
        obj = Credentials.objects.get(platform__name=self.name, identifier=identifier)
        url = posixpath.join(self.base_url, obj.extra_conf['ig_user_id'], "media")
        params = {"access_token": obj.access_token, "media_type": "REELS",
                  "video_url": video_url,
                  "caption": video_caption,
                  "share_to_feed": True,
                  }
        res, is_success = req_api_wrapper("POST", url, params=params, task_name="create_container")
        return res, is_success

    def get_container_status(self, identifier, container_id):
        obj = Credentials.objects.get(platform__name=self.name, identifier=identifier)
        url = posixpath.join(self.base_url, str(container_id))
        params = {"access_token": obj.access_token, "fields": "status_code,status"}
        res, is_success = req_api_wrapper("GET", url, params=params, task_name="container_status", timeout=20)
        return res, is_success

    def publish_container(self, identifier, container_id):
        obj = Credentials.objects.get(platform__name=self.name, identifier=identifier)
        url = posixpath.join(self.base_url, obj.extra_conf["ig_user_id"], "media_publish")
        params = {"access_token": obj.access_token, "creation_id": container_id}
        res, is_success = req_api_wrapper("POST", url, params=params, task_name="media_publish")
        return res, is_success

    def publish_content(self, identifier, **kwargs):
        logger.log(10, msg=f"In instagram_publish content: identifier={identifier}, kwargs={kwargs}")
        res, is_success = self.create_container(identifier,
                                                video_url=kwargs["media_url"],
                                                video_caption=kwargs["media_caption"])
        if is_success:
            while True:
                time.sleep(60)
                res, is_success = self.get_container_status(identifier, container_id=res["id"])
                if is_success and res["status_code"] == "FINISHED":
                    res, is_success = self.publish_container(identifier, container_id=res["id"])
                    break
                elif is_success and res["status_code"] == "ERROR":
                    is_success = False
                    break
        return res, is_success
