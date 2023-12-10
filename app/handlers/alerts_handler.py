import logging
from utils import async_traceback_errors
from aiogram.types import Message
from api.models import get_alerts, add_alert, GetAlerts
from errors import ClientError

logger = logging.getLogger(__name__)


def format_number(number_str: str) -> str:
    if '.' in number_str:
        number_str = number_str.rstrip('0').rstrip('.')
    return number_str


def alert_list(items: list) -> str:
    """Get alerts list

    Args:
        symbols (dict): dict like {id: symbol_name}
        items (list): List of alerts instances

    Returns:
        str: formatted list
    """
    formatted_list = ""
    for index, alert in enumerate(items, start=1):
        formatted_list += f"{index}. {alert['symbol_name']} {alert['trigger']} {format_number(alert['price'])}\n"
        if index > 30:
            formatted_list += '\n...'
            break
    return formatted_list

def format_alert(alert: dict) -> str:
    text = 'Alert added:\n'
    text += f' symbol: {alert['symbol_name']}\n'
    text += f' trigger: {alert['trigger']}\n'
    text += f' price: {alert['price']}\n'
    text += f' created_at: {alert['created_at']}\n'
    return text


@async_traceback_errors(logger)
async def alerts_cmd_handler(message: Message, **kwargs) -> None:
    """Alerts cmd handler"""
    if not message.text:
        raise ValueError('message.text is None')
    if not message.from_user:
        raise ValueError('message.from_user is None')

    alerts = await get_alerts(
        telegram_id=message.from_user.id,
        params=GetAlerts(is_active=True, is_sent=False),
    )
    if alerts:
        await message.answer(f'Alerts:\n{alert_list(alerts)}')
    else:
        await message.answer(f'У вас еще нет ни одного алерта!')


@async_traceback_errors(logger)
async def append_alert(message: Message, **kwargs) -> None:
    if not message.text:
        raise ValueError('message.text is None')
    if not message.from_user:
        raise ValueError('message.from_user is None')

    try:
        words = message.text.split()
        symbol = words[1].upper()
        trigger = words[2].lower()
        price = words[3]

        try:
            comment = words[4:]
            comment = " ".join(comment)
        except IndexError:
            comment = None
    except IndexError:
        raise ClientError(message='Неверный формат добавления алерта!\nВерный:\n add BTCUSDT above 100000')

    await add_alert(
        telegram_id=message.from_user.id,
        broker_name='Binance-spot',
        symbol_name=symbol,
        trigger=trigger,
        price=price,
        comment=comment
    )
    
    alerts = await get_alerts(
        telegram_id=message.from_user.id,
        params=GetAlerts(symbol_name=symbol, is_active=True, is_sent=False),
    )

    await message.answer(f'Alerts:\n{alert_list(alerts)}')