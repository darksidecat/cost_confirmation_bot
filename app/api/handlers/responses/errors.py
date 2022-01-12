from pydantic import Field

from app.api.handlers.responses.base import ApiError


class UserAlreadyExistError(ApiError):
    error = Field("UserAlreadyExists", const=True)
    message = Field("User with this id already exist", const=True)
    user_id: int


class AccessLevelNotFoundError(ApiError):
    error = Field("AccessLevelNotFound", const=True)
    message = Field("Access level for creating user not found", const=True)


class UserNotFoundError(ApiError):
    error = Field("UserNotFound", const=True)
    message = Field("User with this id not found", const=True)
    user_id: int
