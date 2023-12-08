import os

from django.test import TestCase
from .accounts import AccountManager
from .models import Credentials, PlatformInfo


class InstagramCase(TestCase):
    def setUp(self):
        PlatformInfo.objects.create(name='instagram')
        Credentials.objects.create(platform_id=1, identifier="test1")

    def test_list_of_media_instagram(self):
        a = AccountManager("instagram")
        i = a.account_obj
        a = i.get_self_list_of_media("test1")
        print(a)
