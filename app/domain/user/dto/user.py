from typing import List, Optional

from app.domain.common.dto.base import DTO


class UserCreate(DTO):
    id: int
    name: str
    access_levels: List[int]


class PatchUserData(DTO):
    id: Optional[int]
    name: Optional[str]
    access_levels: Optional[list[int]]


class UserPatch(DTO):
    id: int
    user_data: PatchUserData
