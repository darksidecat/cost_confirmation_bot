from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB, Settings
from app.domain.access_levels.models.access_level import AccessLevel
from app.domain.access_levels.models.helper import Levels
from app.domain.user.models.user import TelegramUser
from app.infrastructure.database.repositories.user import logger


def make_connection_string(db: DB, async_fallback: bool = False) -> str:
    result = (
        f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"
    )
    if async_fallback:
        result += "?async_fallback=True"
    return result


def sa_sessionmaker(db: DB, echo: bool = False) -> sessionmaker:
    """
    Make sessionmaker
    :param driver: dialect+driver
    :param db_path: database path and credential
    :return: sessionmaker
    :rtype: sqlalchemy.orm.sessionmaker
    """
    engine = create_async_engine(make_connection_string(db), echo=True)
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True,
        autoflush=False,
    )


async def add_initial_admin(sm: sessionmaker, config: Settings):
    try:
        async with sm() as session:
            administrator_level = AccessLevel(
                id=Levels.ADMINISTRATOR.value.id, name=Levels.ADMINISTRATOR.value.name
            )
            session.add(administrator_level)
            session.add(
                AccessLevel(id=Levels.USER.value.id, name=Levels.USER.value.name)
            )
            session.add(
                AccessLevel(id=Levels.BLOCKED.value.id, name=Levels.BLOCKED.value.name)
            )

            for user_id in config.tg_bot.admin_ids:
                user = TelegramUser(
                    id=user_id,
                    name="Administrator",
                )
                user.access_levels.add(administrator_level)
                session.add(user)

            await session.commit()
            logger.info("Admins added to database")
    except IntegrityError:
        logger.info("Admins already added")
