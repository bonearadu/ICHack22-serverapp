from enum import IntEnum

from rest_framework.exceptions import APIException


class ErrorCodes(IntEnum):
    REGISTER_ID_IN_USE = 100
    USER_DOES_NOT_EXIST = 801


class CustomAPIException(APIException):
    def __init__(self, detail, code):
        self.detail = {'error': detail, 'code': code}
