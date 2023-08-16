from aiogram import Bot, Dispatcher
from handlers import user, set_settings
from config import get_bot_config
from models import db_session
from service import set_bot_commands
import asyncio
import logging


async def main():
    logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG)
    db_session.global_init("db/database.db")

    config = get_bot_config()

    bot = Bot(token=config.bot_token, parse_mode="HTML")
    await set_bot_commands(bot)

    dp = Dispatcher()
    dp.include_router(set_settings.router)
    dp.include_router(user.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена")
        exit(1)
