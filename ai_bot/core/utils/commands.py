from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало/продолжение работы с ботом'
        ),
        # BotCommand(
        #     command='back',
        #     description='Вернуться в главное меню'
        # ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
