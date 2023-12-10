from aiogram.types import Message


async def start_cmd_handler(message: Message, **kwargs):
    """
    This handler receive messages with `/start` command
    Start CMD will register the user and append his settings.
    """

    await message.answer('Я бот для контроля алертов.')
