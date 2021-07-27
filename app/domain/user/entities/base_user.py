from __future__ import annotations

from app.domain.common.entities.entity import Entity


class BaseUser(Entity):
    id: int
    name: str
