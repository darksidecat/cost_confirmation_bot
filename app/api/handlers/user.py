from typing import Union

from fastapi import APIRouter, Depends, Response, status

from app.api import providers
from app.api.handlers.requests.user import UserCreateRequest
from app.api.handlers.responses.errors import (
    AccessLevelNotFoundError,
    UserAlreadyExistError,
    UserNotFoundError,
)
from app.api.handlers.responses.user import Users
from app.domain.access_levels.exceptions.access_levels import AccessLevelNotExist
from app.domain.user.dto.user import PatchUserData, UserCreate, UserPatch
from app.domain.user.exceptions.user import UserAlreadyExists, UserNotExists
from app.domain.user.interfaces.uow import IUserUoW
from app.domain.user.models.user import User
from app.domain.user.usecases.user import (
    AddUser,
    DeleteUser,
    GetUser,
    GetUsers,
    PatchUser,
)

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.get(
    "/", response_model=Users, description="Return users with their access levels"
)
async def get_users(
    uow: IUserUoW = Depends(providers.uow_provider),
):
    users = await GetUsers(uow=uow)()
    return Users(
        users=users,
    )


@user_router.post(
    "/{user_id}",
    responses={
        status.HTTP_201_CREATED: {"model": User},
        status.HTTP_400_BAD_REQUEST: {
            "model": Union[UserAlreadyExistError, AccessLevelNotFoundError]
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    response: Response,
    user_id: int,
    user: UserCreateRequest,
    uow: IUserUoW = Depends(providers.uow_provider),
):
    try:
        user = await AddUser(uow)(UserCreate(id=user_id, **user.dict()))
        return user
    except UserAlreadyExists:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserAlreadyExistError(user_id=user_id)
    except AccessLevelNotExist:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return AccessLevelNotFoundError()


@user_router.delete(
    "/{user_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": UserNotFoundError},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    response: Response,
    uow: IUserUoW = Depends(providers.uow_provider),
):
    try:
        await DeleteUser(uow=uow)(user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotExists:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserNotFoundError(user_id=user_id)


@user_router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": User},
        status.HTTP_400_BAD_REQUEST: {"model": UserNotFoundError},
    },
)
async def get_user(
    user_id: int,
    response: Response,
    uow: IUserUoW = Depends(providers.uow_provider),
):
    try:
        return await GetUser(uow)(user_id=user_id)
    except UserNotExists:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserNotFoundError(user_id=user_id)


@user_router.patch(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": User},
        status.HTTP_400_BAD_REQUEST: {
            "model": Union[
                UserNotFoundError, AccessLevelNotFoundError, UserAlreadyExistError
            ]
        },
    },
)
async def patch_user(
    response: Response,
    user_id: int,
    user_data: PatchUserData,
    uow: IUserUoW = Depends(providers.uow_provider),
):
    try:
        user = await PatchUser(uow)(UserPatch(id=user_id, user_data=user_data))
    except UserNotExists:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserNotFoundError(user_id=user_id)
    except AccessLevelNotExist:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return AccessLevelNotFoundError()
    except UserAlreadyExists:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return UserAlreadyExistError(user_id=user_data.id)
    return user
