import sqlalchemy.orm
from aiogram import Dispatcher

from .database import Database
from .user import UserDB


def setup_middlewares(
    dp: Dispatcher,
    sessionmaker: sqlalchemy.orm.sessionmaker,
):
    dp.update.outer_middleware(Database(sessionmaker))
    dp.update.outer_middleware(UserDB())
