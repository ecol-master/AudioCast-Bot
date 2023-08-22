from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="menu", description="Menu bot actions"),
        BotCommand(command="help", description="Help on using the bot"),
        BotCommand(command="cancel", description="Cancel the last command")
    ]
    await bot.set_my_commands(commands)
