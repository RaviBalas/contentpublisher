import os

import requests
import urllib.parse

from django.conf import settings

from core.settings import PUBLIC_URL
from .account import Account
from social_media.models import Credentials

from .account import Account
import yt_dlp
import random


class Youtube(Account):
    def __init__(self, *args, **kwargs):
        self.name = "youtube"
        self.base_url = settings.YOUTUBE_ENDPOINT
        super(Youtube, self).__init__(*args, **kwargs)

    def generate_public_url(self, social_media_url):
        is_success = False
        try:
            saved_path = os.path.join(settings.BASE_DIR, 'media')
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f'{saved_path}/VIDEO_{random.randint(1000, 9999)}.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(social_media_url, download=True)
                title = info_dict['title']
                outtmpl_value = ydl_opts['outtmpl']
                default_value = outtmpl_value["default"]
                video_basename = os.path.splitext(os.path.basename(default_value))[0]
                video_filename = f"{video_basename}.mp4"
                full_path = os.path.join(saved_path, video_filename)
                public_url = os.path.join(PUBLIC_URL, 'media/', video_filename)
                if public_url:
                    is_success = True
                    res = {
                        'public_url': public_url,
                        'title': title,
                    }
                    print(f"Video saved at: {full_path}")
                else:
                    res = {"message": "Something went wrong, couldn't download the video"}
        except Exception as e:
            print(f"An error occurred: {e}")
            res = None
        return res, is_success

    def publish_content(self, identifier, **kwargs):
        pass  # return res, is_success
