from enum import IntEnum

from rest_framework.exceptions import APIException


class ErrorCodes(IntEnum):
    GAME_STARTED = 300
    REGISTER_ID_IN_USE = 100
    USER_DOES_NOT_EXIST = 801
    MISSING_ID = 200
    ID_NOT_GM = 201


class CustomAPIException(APIException):
    def __init__(self, detail, code):
        self.detail = {'error': detail, 'code': code}
