from __future__ import annotations

from app.domain.common.models.entity import Entity


class BaseUser(Entity):
    id: int
    name: str
