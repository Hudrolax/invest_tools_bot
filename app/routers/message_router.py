from aiogram import Router, types
import logging
from handlers.alerts_handler import alerts_cmd_handler, append_alert

logger = logging.getLogger(__name__)

message_router = Router()


@message_router.message()
async def message_handler(message: types.Message, **kwargs) -> None:
    if message.from_user is None:
        logger.info('Got message not from a user.')
        return

    if message.text:
        if message.text.startswith('alerts'):
            await alerts_cmd_handler(message, **kwargs)

        elif message.text.startswith('add '):
            await append_alert(message, **kwargs)
