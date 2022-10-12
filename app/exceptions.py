from rest_framework.exceptions import APIException
from rest_framework import status


class Exceptions(APIException):
    pass


class InvalidNumber(Exceptions):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail):
        super().__init__(detail)


class DoesNotExist(Exceptions):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail=None):
        super().__init__(detail, 'does_not_exist')


class AlreadyExists(Exceptions):
    def __init__(self, detail):
        super().__init__(detail)


class DeletionFailed(Exceptions):
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class UpdationFailed(Exceptions):
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class AttendanceAlreadyMarked(Exceptions):
    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class AuthenticationFailed(Exceptions):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class AccessDenied(Exceptions):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class InvalidFormat(Exceptions):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
