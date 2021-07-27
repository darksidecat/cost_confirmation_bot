from typing import List

from pydantic import BaseModel

from app.domain.access_levels.entities.access_level import AccessLevel


class AccessLevels(BaseModel):
    access_levels: List[AccessLevel]
