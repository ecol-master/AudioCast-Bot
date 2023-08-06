from aiogram import Bot, Dispatcher
from handlers import user
from config import get_bot_config
import asyncio
import logging


async def main():
    logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG)

    config = get_bot_config()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    dp.include_router(user.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена")
        exit(1)
