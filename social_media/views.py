import time

from rest_framework.response import Response
from rest_framework.views import APIView

from common.db_log_handler import log_error
from .accounts import AccountManager


# Error-Code: 3000
# Create your views here.
class Testview(APIView):
    def get(self, request):
        try:
            data = self.request.query_params
            if data.get("key") == "list_media":
                acc_inst = AccountManager("instagram")
                insta_obj = acc_inst.account_obj
                response = insta_obj.get_self_list_of_media("app1")
                return Response({"key": data["key"], "data": response}, status=200)
            elif data.get("key") == "video_download":
                acc_inst = AccountManager("youtube")
                insta_obj = acc_inst.account_obj
                response = insta_obj.generate_public_url("https://youtube.com/shorts/46mIjzoGyG4?si=DWC-lWfoXFyCwWFy")
                return Response({"key": data["key"], "data": response}, status=200)
            elif data.get("key") == "create_container":
                acc_inst = AccountManager("instagram")
                insta_obj = acc_inst.account_obj
                response = insta_obj.create_container("app1",
                                                      video_url=request.data["video_url"],
                                                      video_caption=request.data["video_caption"])
                return Response({"key": data["key"], "data": response})
            elif data.get("key") == "container_status":
                acc_inst = AccountManager("instagram")
                insta_obj = acc_inst.account_obj
                response = insta_obj.get_container_status("app1", container_id=request.data.get("container_id"))
                return Response({"key": data["key"], "data": response})
            elif data.get("key") == "media_publish":
                acc_inst = AccountManager("instagram")
                insta_obj = acc_inst.account_obj
                response = insta_obj.publish_container("app1", container_id=request.data.get("container_id"))
                return Response({"key": data["key"], "data": response})
            else:
                keys = ["list_media", "create_container", "container_status", "media_publish", "video_download"]
                return Response({"error": "please pass atleast one key", "data": keys}, status=400)
        except Exception as e:
            log_error(e, 3500)
            return Response({"error": str(e)}, status=500)


class InstagramView(APIView):

    def get(self, request):
        acc_inst = AccountManager("instagram")
        insta_obj = acc_inst.account_obj
        response = insta_obj.get_self_list_of_media(request.query_params.get("identifier"))
        return Response({"data": response}, status=200)

    def post(self, request):
        acc_inst = AccountManager("instagram")
        insta_obj = acc_inst.account_obj
        res, is_success = insta_obj.publish_content(request.query_params.get("identifier"),
                                                    url=request.data["url"],
                                                    caption=request.data["caption"])
        return Response({"data": res}, status=200 if is_success else 400)
