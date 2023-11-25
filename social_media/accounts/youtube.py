import requests
import urllib.parse

from django.conf import settings

from .account import Account
from social_media.models import Credentials

from .account import Account


class Youtube(Account):
    def __init__(self, *args, **kwargs):
        self.name = "youtube"
        self.base_url = settings.YOUTUBE_ENDPOINT
        super(Youtube, self).__init__(*args, **kwargs)
