from app.domain.common.exceptions.base import AppException


class OrderException(AppException):
    """Base Order Exception"""


class ConfirmationAlreadyProcessed(OrderException):
    """Order already confirmed, denied and can't be processed again"""


class OrderNotConfirmed(OrderException):
    """Order not confirmed yet"""
