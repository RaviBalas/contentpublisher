import os
import posixpath
import random
import yt_dlp

from django.conf import settings

from common.utils import req_api_wrapper
from social_media.models import Credentials
from social_media.initial_mapping import youtube_video_category_mapping
from .account import Account


class Youtube(Account):
    def __init__(self, *args, **kwargs):
        self.name = "youtube"
        self.base_url = settings.YOUTUBE_ENDPOINT
        self.category_mapping = youtube_video_category_mapping
        super(Youtube, self).__init__(*args, **kwargs)

    @classmethod
    def filter_with_type(cls, media_obj, media_type):
        if media_type == "shorts":
            if "shorts" in media_obj["name"].lower() or "shorts" in media_obj["description"].lower():
                return True
            url = f"https://yt.lemnoslife.com/videos?part=short&id={media_obj['url']}"
            res, is_success = req_api_wrapper("GET", url, save_log=False)
            if is_success:
                return res["items"]["short"]["available"]

    def list_of_social_media_listing(self, category, identifier, **kwargs):
        """
        API:https://developers.google.com/youtube/v3/docs/search/list
        params:
            q: The q parameter specifies the query term to search for
            pageToken:  to navigate next or prev page.
            videoCategoryId:   id of category
            order: date, rating, relevance, title, videoCount, viewCount
        """
        obj = Credentials.objects.get(platform__name=self.name, identifier=identifier)
        url = posixpath.join(self.base_url, "youtube/v3/search")
        params = {"key": obj.api_key,
                  "part": "snippet",
                  "type": "video",
                  "videoDuration": "short",
                  "maxResults": kwargs.pop("page_size", 50),
                  "regionCode": "IN",
                  "order": "viewCount"
                  }
        if category.lower() in self.category_mapping:
            params["videoCategoryId"] = self.category_mapping[category.lower()]
        if kwargs.get("q", None):
            params["q"] = kwargs.pop("q")
        if "next_page" in kwargs:
            params["pageToken"] = kwargs.pop("next_page")
        params.update(kwargs)
        res, is_success = req_api_wrapper("GET", url, params=params, task_name="youtube_listing")
        if is_success:
            response = {"next_page": res["nextPageToken"]}
            media_list = []
            for i in res["items"]:
                media_list.append({"url": f"https://www.youtube.com/shorts/{i['id']['videoId']}",
                                   "title": i["snippet"]["title"],
                                   "description": i["snippet"]["description"]})
            response["media_list"] = media_list
            return response, is_success
        return res, is_success

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
                public_url = os.path.join(settings.BACKEND_PUBLIC_URL, 'media/', video_filename)
                res, is_success = {'url': public_url, "media_type": 'reels', 'name': title}, True
        except Exception as e:
            res = str(e)
        return res, is_success

    def publish_content(self, identifier, **kwargs):
        pass  # return res, is_success
