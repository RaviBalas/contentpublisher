import json
import time

import requests
from django.utils import timezone

from common.db_log_handler import log_error
from common.models import ApiLogsModel
import logging

logger = logging.getLogger("db")


def save_logs(created_datetime, task_name=None, request_type=None, params=None, url=None, data=None, files=None,
              json_body=None,
              response=None, status_code=None, error=None):
    try:
        completion_datetime = timezone.now()
        logger.debug(msg=f"{task_name} > saving logs")
        time_taken = (completion_datetime - created_datetime).seconds
        api_obj = {"time_taken": time_taken, "task_name": task_name, "request_type": request_type,
                   "url": url, "status_code": status_code, "error": error}
        if isinstance(data, dict) and data:
            api_obj["data"] = json.dumps(data)
        if isinstance(params, dict) and params:
            api_obj["param"] = json.dumps(params)
        if isinstance(json_body, dict) and json_body:
            api_obj["json"] = json.dumps(json_body)
        if isinstance(response, dict) and response:
            api_obj["response"] = json.dumps(response)
        ApiLogsModel.objects.create(**api_obj)
    except Exception as e:
        log_error(e, 1500)


def req_api_wrapper(request_type, url, json_data=None, headers=None, data=None, params=None, task_name="",
                    files=None, timeout=120, save_log=True, retry_count=1):
    count = 0
    error = None
    is_success = False
    res = None
    while count < retry_count:
        created_datetime = timezone.now()
        try:
            response = requests.request(request_type, url, data=data, json=json_data, headers=headers, params=params,
                                        files=files, timeout=timeout)
            status_code = response.status_code
            if status_code in [200, 201]:
                res = response.json()
                is_success = True
                count = retry_count
                error = None
            else:
                is_success = False
                res = response.text
                count = retry_count + 1
        except Exception as e:
            is_success = False
            count = retry_count + 1
            error = str(e)
            print("Except Exception as e while calling api", str(e))
            status_code = 500
            res = str(e)
        if save_log:
            save_logs(created_datetime, task_name=task_name, request_type=request_type, url=url, data=data, files=files,
                      params=params, json_body=json_data, response=res, status_code=status_code, error=error)
        time.sleep(5)
    return res, is_success
