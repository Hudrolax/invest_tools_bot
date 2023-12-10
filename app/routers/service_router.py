from aiogram import Router
from aiogram.filters import Command

from handlers.start_handler import start_cmd_handler
from handlers.alerts_handler import alerts_cmd_handler

router = Router()

router.message.register(start_cmd_handler, Command('start'))
router.message.register(alerts_cmd_handler, Command('alerts'))
