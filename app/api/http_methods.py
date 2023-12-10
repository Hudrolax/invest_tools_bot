import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from typing import Literal, Annotated
import json
import logging

from config import BACKEND_ROOT_PATH, BACKEND_SECRET
from errors import BackendError, ConnectionError


logger = logging.getLogger(__name__)


async def request(
    method: Literal['get', 'post', 'put', 'delete'],
    endpoint: Annotated[str, 'Request endpoint'],
    telegram_id: int | None = None,
    **kwargs
) -> dict | list:
    async with aiohttp.ClientSession() as session:
        headers = {
            'Content-Type': 'application/json',
            'TBOT-SECRET': BACKEND_SECRET,
        }
        if telegram_id:
            headers['TELEGRAM-ID'] = str(telegram_id)

        if kwargs.get('data') and isinstance(kwargs.get('data'), dict):
            kwargs['data'] = json.dumps(kwargs['data'], ensure_ascii=False)
        
        if kwargs.get('params'):
            kwargs['params'] = {k: str(v).lower() if isinstance(v, bool) else v for k, v in kwargs['params'].items()}

        try:
            async with session.request(
                method=method,
                headers=headers,
                url=f'http://{BACKEND_ROOT_PATH}' + endpoint,
                timeout=3,
                **kwargs
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    logger.error(f"Backend request failed with status {resp.status}. Body: {await resp.text()}")
                    raise BackendError(message=f'Error {await resp.text()}', status=resp.status)
        except ClientConnectorError as e:
            logger.error(f"Backend request failed with error: {e}")
            raise ConnectionError('Ошибка подключения к backend')
