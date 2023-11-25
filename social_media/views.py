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
                response = insta_obj.get_list_of_media("app1")
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
                keys = ["list_media", "create_container", "container_status", "media_publish"]
                return Response({"error": "please pass atleast one key", "data": keys}, status=400)
        except Exception as e:
            log_error(e, 3500)
            return Response({"error": str(e)}, status=500)


class InstagramView(APIView):

    def get(self, request):
        acc_inst = AccountManager("instagram")
        insta_obj = acc_inst.account_obj
        response = insta_obj.get_list_of_media("app1")
        return Response({"data": response}, status=200)

    def post(self, request):
        acc_inst = AccountManager("instagram")
        insta_obj = acc_inst.account_obj
        res, is_success = insta_obj.create_container("app1",
                                                     video_url=request.data["video_url"],
                                                     video_caption=request.data["video_caption"])
        if not is_success:
            return Response({"data": res}, 400)
        while True:
            res, is_success = insta_obj.get_container_status("app1", container_id=res["id"])
            time.sleep(5)
            if res["status_code"] == "FINISHED":
                break
        res, is_success = insta_obj.publish_container("app1", container_id=res["id"])
        return Response({"data": res}, status=200 if is_success else 400)
