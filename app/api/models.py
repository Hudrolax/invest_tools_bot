from typing import Literal
from pydantic import BaseModel

from .http_methods import request


class GetAlerts(BaseModel):
    symbol_id: int | None = None
    symbol_name: str | None = None
    is_sent: bool | None = None
    is_active: bool | None = None
    is_triggered: bool | None = None


async def get_user(user_id: int) -> dict:
    user = await request(
        method='get',
        endpoint=f'/users/telegram_bot_api/{user_id}'
    )
    if not isinstance(user, dict):
        raise ValueError('Result is not a dict')
    return user


async def delete_alert(telegram_id: int, alert_id: int) -> bool:
    kwargs = dict(
        method='delete',
        endpoint=f'/alerts/{alert_id}',
        telegram_id=telegram_id,
    )
    return await request(**kwargs) # type: ignore


async def get_alerts(
    params: GetAlerts,
    telegram_id: int | None = None,
) -> list:
    kwargs = dict(
        method='get',
        endpoint='/alerts',
        params=params.model_dump(exclude_unset=True),
    )
    if telegram_id:
        kwargs['telegram_id'] = telegram_id # type: ignore
    else:
        kwargs['endpoint'] += '/telegram_bot_api/' # type: ignore
    
    alerts = await request(**kwargs) # type: ignore
    if not isinstance(alerts, list):
        raise TypeError('Result is not a list')
    return alerts


async def add_alert(
    telegram_id: int,
    broker_name: Literal['Binance-spot'],
    symbol_name: str,
    trigger: str,
    price: str,
    comment: str | None = None,
) -> dict:
    payload = dict(
        broker_name=broker_name,
        symbol_name=symbol_name,
        trigger=trigger,
        price=price,
        comment=comment
    )
    alert = await request(
        method='post',
        endpoint='/alerts',
        telegram_id=telegram_id,
        json=payload,
    )
    if not isinstance(alert, dict):
        raise ValueError('Result is not a dict')

    return alert


async def mark_alert_id_sent(telegram_id: int, alert_id: int):
    alert = await request(
        method='put',
        endpoint=f'/alerts/{alert_id}',
        telegram_id=telegram_id,
        json=dict(is_sent=True, is_active=False),
    )
    if not isinstance(alert, dict):
        raise ValueError('Result is not a dict')

    return alert