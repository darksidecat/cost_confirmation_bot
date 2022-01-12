from typing import List

from pydantic import BaseModel

from app.domain.user.models.user import User


class Users(BaseModel):
    users: List[User]
