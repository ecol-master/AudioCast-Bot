from aiogram import Bot, Dispatcher
from handlers import user
import logging
import asyncio
from config import get_config
import yt_dlp


async def main():
    logging.basicConfig(level=logging.INFO)

    config = get_config()
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
