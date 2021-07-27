from pydantic import BaseModel


class ApiError(BaseModel):
    error: str
    message: str


class ErrorResponse(BaseModel):
    error = ApiError
