from fastapi import APIRouter, Depends

from app.api import providers
from app.api.handlers.responses.access_levels import AccessLevels
from app.domain.access_levels.interfaces.uow import IAccessLevelUoW
from app.domain.access_levels.usecases.access_levels import GetAccessLevels

access_levels_router = APIRouter(
    prefix="/access_level",
    tags=["access_level"],
)


@access_levels_router.get("/", response_model=AccessLevels)
async def get_access_levels(
    uow: IAccessLevelUoW = Depends(providers.uow_provider),
) -> AccessLevels:
    access_levels = await GetAccessLevels(uow)()
    return AccessLevels(access_levels=access_levels)
