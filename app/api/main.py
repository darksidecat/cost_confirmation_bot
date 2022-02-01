import logging

from fastapi import FastAPI

from app.api import providers
from app.api.handlers import access_levels, user
from app.api.middlewares.db_session import DatabaseSessionMiddleware
from app.config import load_config
from app.infrastructure.database.db import sa_sessionmaker
from app.infrastructure.database.models.user import map_tables
from app.infrastructure.event_dispatcher import configure_dispatch


def api():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    app = FastAPI()

    config = load_config()
    session_factory = sa_sessionmaker(config.db)
    map_tables()

    app.add_middleware(DatabaseSessionMiddleware, session_factory=session_factory)
    app.include_router(user.user_router)
    app.include_router(access_levels.access_levels_router)

    event_dispatcher = configure_dispatch()

    app.dependency_overrides[providers.uow_provider] = providers.uow
    app.dependency_overrides[providers.user_provider] = providers.user
    app.dependency_overrides[providers.access_policy_provider] = providers.access_policy
    app.dependency_overrides[
        providers.event_dispatcher_provider
    ] = lambda: event_dispatcher
    app.dependency_overrides[providers.user_service_provider] = providers.user_service

    return app
