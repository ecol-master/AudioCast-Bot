from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="help", description="Справка по использованию бота."),
        BotCommand(command="set_caption",
                   description="Установить длину описания к подкасту.")
    ]
    await bot.set_my_commands(commands)
