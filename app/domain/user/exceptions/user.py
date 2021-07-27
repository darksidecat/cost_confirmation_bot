from app.domain.common.exceptions.base import AppException


class UserException(AppException):
    """Base User Exception"""


class UserAlreadyExist(UserException):
    """User already exist"""


class UserNotExist(UserException):
    """User not exist"""
