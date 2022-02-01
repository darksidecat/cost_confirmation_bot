import logging
from typing import Any, Dict

from app.domain.common.events.dispatcher import EventDispatcher
from app.domain.user.models.user import UserCreated

logger = logging.getLogger(__name__)


async def user_created_handler(event: UserCreated, data: Dict[str, Any]):
    logger.info("Created user %s", event.user)


def configure_dispatch():
    event_dispatcher = EventDispatcher()
    event_dispatcher.register_notify(UserCreated, user_created_handler)
    event_dispatcher.register_notify(UserCreated, user_created_handler)
    return event_dispatcher
