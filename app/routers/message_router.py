from aiogram import Router, types
import logging
from handlers.alerts_handler import (
    alerts_cmd_handler,
    append_alert,
    alerts_by_symbol,
    del_alert,
)

logger = logging.getLogger(__name__)

message_router = Router()


@message_router.message()
async def message_handler(message: types.Message, **kwargs) -> None:
    if message.from_user is None:
        logger.info('Got message not from a user.')
        return

    if not message.text:
        logger.info('Got message without text.')
        return

    
    text = message.text.lower()

    if message.text:
        if text.startswith('alerts'):
            await alerts_cmd_handler(message, **kwargs)

        elif text.startswith('add ') or '>' in text or '<' in text:
            await append_alert(message, **kwargs)

        elif message.text.startswith('del '):
            await del_alert(message, **kwargs)
        
        else:
            await alerts_by_symbol(message, **kwargs)
