from typing import List

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    name: str
    access_levels: List[int]
