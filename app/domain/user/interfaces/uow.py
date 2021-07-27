from app.domain.common.interfaces.uow import IUoW
from app.domain.user.interfaces.repo import IUserRepo


class IUserUoW(IUoW):
    user: IUserRepo
