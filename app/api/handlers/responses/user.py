from typing import List

from pydantic import BaseModel

from app.domain.user.entities.user import User


class Users(BaseModel):
    users: List[User]
