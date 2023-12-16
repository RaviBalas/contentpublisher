import os
import posixpath
import random
import string
from datetime import datetime

import yt_dlp

from django.conf import settings

from common.utils import req_api_wrapper
from social_media.models import Credentials
from social_media.initial_mapping import youtube_video_category_mapping
from .account import Account
import concurrent.futures


class Youtube(Account):
    def __init__(self, *args, **kwargs):
        self.name = "youtube"
        self.base_url = settings.YOUTUBE_ENDPOINT
        self.category_mapping = youtube_video_category_mapping
        super(Youtube, self).__init__(*args, **kwargs)

    @classmethod
    def filter_with_type(cls, media_obj, media_type):
        try:
            if media_type == "shorts":
                if "shorts" in media_obj["title"].lower() or "shorts" in media_obj["description"].lower():
                    return True
                else:
                    url = f"https://yt.lemnoslife.com/videos?part=short&id={media_obj['url']}"
                    res, is_success = req_api_wrapper("GET", url, save_log=False)
                    if is_success:
                        short_info = res.get("items", {}).get("short", {})
                        if "available" in short_info:
                            return short_info["available"]
                        else:
                            return "Error: 'available' key not found in the API response.", False
                    else:
                        return "API request failed", False
        except Exception as e:
            return "An unexpected error occurred:", e

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
                print("media_list", media_list)
            response["media_list"] = media_list
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for i in media_list:
                    future = executor.submit(self.filter_with_type, i, 'shorts')
                    futures.append(future)
                futures = [executor.submit(self.filter_with_type, i, 'shorts') for i in media_list]
                concurrent.futures.wait(futures)
                results = []
                for future in futures:
                    result = future.result()
                    results.append(result)
                shorts_available_list = [result for result in results if result]
            response["shorts_available_list"] = shorts_available_list
            print("shorts_available_list", shorts_available_list)
            print("response", response)
            return response, is_success
        return res, is_success

    def generate_public_url(self, social_media_url):
        is_success = False
        try:
            media_root = os.path.join(settings.BASE_DIR, 'media')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            random_str = "".join(random.choices(string.ascii_letters + string.digits, k=16))
            ydl_opts = {
                'format': 'bestvideo[height<=1920]+bestaudio/best[height<=1920]',
                'outtmpl': f'{media_root}/VIDEO_{timestamp}_{random_str}.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(social_media_url, download=True)
                outtmpl_value = ydl_opts['outtmpl']
                default_value = outtmpl_value["default"]
                video_basename = os.path.splitext(os.path.basename(default_value))[0]
                video_filename = f"{video_basename}.mp4"
                local_url = os.path.join(media_root, 'media', video_filename)
                os.system(
                    f"ffmpeg -i {local_url} -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 192k -movflags +faststart -y {local_url}")

                res, is_success = {'url': os.path.join(settings.BACKEND_PUBLIC_URL, 'media', video_filename),
                                   "media_type": 'reels',
                                   'name': info_dict['title']
                                   }, True
        except Exception as e:
            res = str(e)
        finally:
            pass
            # todo: Remove temp file
            # if os.path.exists(original_video_path):
            #     os.remove(original_video_path)
        return res, is_success

    def publish_content(self, identifier, **kwargs):
        pass  # return res, is_success
