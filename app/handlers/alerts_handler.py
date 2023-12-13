import logging
from utils import async_traceback_errors
from aiogram.types import Message
from api.models import get_alerts, add_alert, GetAlerts, delete_alert
from errors import ClientError
from . import current_alerts_list

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
    current_alerts_list.clear()
    for i, alert in enumerate(items, start=1):
        # add to current list
        current_alerts_list[str(i)] = alert['id']

        _symbol = alert['symbol_name']
        _trigger = alert['trigger']
        _price = format_number(alert['price'])
        _active = '' if alert['is_active'] else ' INACTIVE'

        formatted_list += f"{i}. {_symbol} {_trigger} {_price}{_active}\n"
        # if i > 30:
        #     formatted_list += '\n...'
        #     break

    return formatted_list


@async_traceback_errors(logger)
async def del_alert(message: Message, **kwargs) -> None:
    """Returns alerts list by symbol"""
    if not message.text:
        raise ValueError('message.text is None')
    if not message.from_user:
        raise ValueError('message.from_user is None')

    try:
        words = message.text.split()
        alert_number = words[1].upper()
        alert_id = current_alerts_list[alert_number]
    except IndexError:
        raise ClientError(message='Неверный формат удаления. Надо: del BTCUSDT')
    except KeyError:
        raise ClientError(message='Нет такого номера алерта. Попробуйте вывести список алертов через команду alerts или имя символа.')

    await delete_alert(telegram_id=message.from_user.id, alert_id=alert_id)

    alerts = await get_alerts(
        telegram_id=message.from_user.id,
        params=GetAlerts(),
    )
    if alerts:
        await message.answer(f'Alerts:\n{alert_list(alerts)}')
    else:
        await message.answer(f'У вас еще нет ни одного алерта!')
        

@async_traceback_errors(logger)
async def alerts_by_symbol(message: Message, **kwargs) -> None:
    """Returns alerts list by symbol"""
    if not message.text:
        raise ValueError('message.text is None')
    if not message.from_user:
        raise ValueError('message.from_user is None')


    alerts = await get_alerts(
        telegram_id=message.from_user.id,
        params=GetAlerts(symbol_name=message.text.upper()),
    )
    if alerts:
        await message.answer(f'Alerts:\n{alert_list(alerts)}')
    else:
        await message.answer(f'У вас еще нет ни одного алерта!')


@async_traceback_errors(logger)
async def alerts_cmd_handler(message: Message, **kwargs) -> None:
    """Alerts cmd handler"""
    if not message.text:
        raise ValueError('message.text is None')
    if not message.from_user:
        raise ValueError('message.from_user is None')

    alerts = await get_alerts(
        telegram_id=message.from_user.id,
        params=GetAlerts(),
    )
    if alerts:
        await message.answer(f'Alerts:\n{alert_list(alerts)}')
    else:
        await message.answer(f'У вас еще нет ни одного алерта!')


@async_traceback_errors(logger)
async def append_alert(message: Message, **kwargs) -> None:
    """A message handler for adding a new alert"""
    if not message.text:
        raise ValueError('message.text is None')
    if not message.from_user:
        raise ValueError('message.from_user is None')

    try:
        words = message.text.split()
        symbol = words[1].upper()
        trigger = words[2].lower().replace('>', 'above').replace('<', 'below')
        price = words[3].replace(',', '.')


        try:
            comment = words[4:]
            comment = " ".join(comment)
        except IndexError:
            comment = None
    except IndexError:
        text = 'Неверный формат добавления алерта!\n'
        text += 'Пример:\n add BTCUSDT above (below) 100000 комментарий к алерту\n'
        text += 'или add ethusdt < купить немного ETH'
        raise ClientError(message=text)

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

    await message.answer(f'{symbol} alerts:\n{alert_list(alerts)}')