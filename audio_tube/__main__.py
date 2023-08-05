from aiogram import Bot, Dispatcher
from handlers import user
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from service import del_downloaded_files
from config import get_bot_config
import asyncio
import logging


async def main():
    logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(del_downloaded_files, 'interval', minutes=5)

    config = get_bot_config()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    dp.include_router(user.router)

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена")
        exit(1)
