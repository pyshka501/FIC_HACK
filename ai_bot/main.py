import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from ai_bot.core.handlers.gen_func import router_gen
from ai_bot.core.handlers.memory_page_hand import router_mp
from core.handlers.basic import router_handler

from core.settings import get_settings
from core.utils.commands import set_commands

settings = get_settings("core\\input")

from core.middlewares.db import DataBaseSession
from core.database.engine import create_db, session_maker




async def on_startup(bot: Bot):
    await create_db()
    try:
        await bot.send_message(settings.bots.admin_id, text='start')
        await set_commands(bot)
    except Exception as ex:
        print(ex, "   ||| ERROR")


async def on_offline(bot: Bot):
    try:
        await bot.send_message(settings.bots.admin_id, text='offline')
    except Exception as ex:
        print(ex, "   ||| ERROR")


async def start():
    bot = Bot(
        token=settings.bots.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    bot.admin_id = settings.bots.admin_id


    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_offline)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.include_routers(router_handler, router_mp, router_gen)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("EXIT")
