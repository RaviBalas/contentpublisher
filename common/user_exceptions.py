from rest_framework import status
from rest_framework.exceptions import APIException


class GenericException(APIException):
    default_code = 1000
    default_detail = "There is some issue. Please contact support"


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 1400
    default_detail = 'Bad Request'
