import argparse
import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import DialogRegistry
from aiogram_dialog.tools import render_preview, render_transitions

from app.config import load_config
from app.infrastructure.database.db import add_initial_admin, sa_sessionmaker
from app.tgbot.handlers import register_handlers
from app.tgbot.middlewares import setup_middlewares
from app.tgbot.services.set_commands import set_commands

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dev",
        help="Run bot in dev mode",
        action="store",
        nargs="*",
    )
    parser.add_argument(
        "--init_admin_db",
        action="store",
        help="Add admins to database from config file",
        nargs="*",
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config(env_file=".env.dev" if args.dev is not None else None)

    if config.tg_bot.use_redis:
        storage = RedisStorage.from_url(
            url=f"redis://{config.redis.host}",
            connection_kwargs={
                "db": config.redis.db,
            },
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    else:
        storage = MemoryStorage()

    session_factory = sa_sessionmaker(config.db, echo=False)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage, isolate_events=True)
    admin_router = Router()
    dp.include_router(admin_router)

    dialog_registry = DialogRegistry(dp)

    setup_middlewares(
        dp=dp,
        sessionmaker=session_factory,
    )

    register_handlers(dp=dp, admin_router=admin_router, dialog_registry=dialog_registry)

    if args.init_admin_db is not None:
        await add_initial_admin(session_factory, config)

    try:
        # render_transitions(dialog_registry, title="Cost confirmation bot")
        await set_commands(bot, config)
        await dp.start_polling(bot, config=config)
    finally:
        await dp.fsm.storage.close()
        await bot.session.close()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logger.error("Bot stopped!")
