import logging
from utils import async_traceback_errors
from aiogram.types import Message

logger = logging.getLogger(__name__)


@async_traceback_errors(logger)
async def help_cmd_handler(message: Message, **kwargs) -> None:
    """Help cmd handler"""
    
    text = '```Help:'
    text += ' alerts: Вывести список всех алертов\n'
    text += ' add <symbol_name> above(or below) <price> <comment>: Добавить новый алерт\n'
    text += ' <symbol_name>: Вывести список алертов для символа\n'
    text += ' del <N>: удалить алерт номер <N> из предыдущего списка алертов\n'
    text += '```'
    await message.answer(text, parse_mode='Markdown')