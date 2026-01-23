# accesshub/exceptions.py

from rest_framework.exceptions import APIException
from rest_framework import status


class InactiveUserException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "User account is not activated."
    default_code = "user_inactive"
