import asyncio
from aiogram import Dispatcher, Router

from bot import bot, get_bot_commands
import config
from middleware import MessageMiddleware
from routers.service_router import router as service_router
from routers.message_router import message_router

from tasks import task_check_alerts

dp = Dispatcher()

router = Router()
router.include_routers(
    service_router,
    message_router,
)

dp.include_router(router)
dp.message.middleware(MessageMiddleware())

stop_event = asyncio.Event()


@dp.shutdown()
async def on_shutdown(*args, **kwargs):
    stop_event.set()


async def main() -> None:
    bot_commands_ru = get_bot_commands()
    await bot.set_my_commands(commands=bot_commands_ru)
    await bot.set_chat_menu_button()

    await asyncio.gather(
        dp.start_polling(bot),
        task_check_alerts(bot, stop_event),
    )

if __name__ == "__main__":
    asyncio.run(main())
