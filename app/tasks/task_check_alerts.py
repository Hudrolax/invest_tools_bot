import asyncio
from aiogram import Bot
import logging

from api.models import get_alerts, GetAlerts, get_user, mark_alert_id_sent
from handlers.alerts_handler import format_number


logger = logging.getLogger(__name__)


async def task_check_alerts(
    bot: Bot,
    stop_event: asyncio.Event,
) -> None:
    await asyncio.sleep(5)
    logger.info('Start task check alerts')
    while not stop_event.is_set():
        try:
            triggered_alerts = await get_alerts(GetAlerts(is_sent=False, is_active=True, is_triggered=True))
            for alert in triggered_alerts:
                user = await get_user(user_id=alert['user_id'])
                text = f'{alert["symbol_name"]} is {alert["trigger"]} {
                    format_number(alert["price"])}\nComment: {alert["comment"]}'
                try:
                    await bot.send_message(
                        chat_id=user['telegram_id'],
                        text=text
                    )
                    await mark_alert_id_sent(telegram_id=user['telegram_id'], alert_id=alert['id'])

                except:
                    pass

            await asyncio.sleep(5)
        except Exception as ex:
            logger.critical(str(ex))
            await asyncio.sleep(5)
