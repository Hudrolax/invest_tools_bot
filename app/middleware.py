from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any, Awaitable
from errors import BackendError, ConnectionError, ClientError


class MessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except (BackendError, ConnectionError, ClientError) as e:
            await event.answer(f"```Ошибка\n{e.message}\n```", parse_mode='Markdown')
        except Exception as ex:
            await event.answer('Неизвестная ошибка!')
