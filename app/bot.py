from aiogram import Bot
from aiogram.types import BotCommand
from config import TELEGRAM_API_KEY


def get_bot_commands() -> list[BotCommand]:
    return [
        BotCommand(command='/start', description='Start cmd'),
        BotCommand(command='/alerts', description='Alerts list'),
        BotCommand(command='/help', description='Help'),
    ]


bot = Bot(TELEGRAM_API_KEY, parse_mode="HTML")
