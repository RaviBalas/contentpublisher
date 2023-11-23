import json

from django.utils import timezone

from common.db_log_handler import log_error
from common.models import ApiLogsModel


def save_logs(created_datetime, task_name=None, request_type=None, url=None, data=None, files=None, json_body=None,
              response=None, status_code=None, error=None):
    try:
        completion_datetime = timezone.now()
        print("saving logs")
        time_taken = (completion_datetime - created_datetime).seconds
        api_obj = {"time_taken": time_taken, "task_name": task_name, "request_type": request_type,
                   "url": url, "status_code": status_code, "error": error}
        if isinstance(data, dict) and data:
            api_obj["data"] = json_body.dumps(data)
        if isinstance(json_body, dict) and json_body:
            api_obj["json"] = json.dumps(json_body)
        if isinstance(response, dict) and response:
            api_obj["response"] = json_body.dumps(response)
        ApiLogsModel.objects.create(**api_obj)
    except Exception as e:
        log_error(e, 1500)
