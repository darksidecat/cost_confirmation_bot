from fastapi import FastAPI

from app.api.handlers import access_levels, user
from app.api.middlewares.db_session import DatabaseSessionMiddleware
from app.api.providers import get_uow, uow_provider
from app.config import load_config
from app.infrastructure.database.db import sa_sessionmaker
from app.infrastructure.database.models.user import map_tables


def api():
    app = FastAPI()

    config = load_config()
    session_factory = sa_sessionmaker(config.db)
    map_tables()

    app.add_middleware(DatabaseSessionMiddleware, session_factory=session_factory)
    app.include_router(user.user_router)
    app.include_router(access_levels.access_levels_router)

    app.dependency_overrides[uow_provider] = get_uow

    return app
