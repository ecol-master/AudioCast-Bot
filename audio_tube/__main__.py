from aiogram import Bot, Dispatcher
from handlers import user
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
from config import get_config
from utils.schedule import del_downloaded_files


async def main():
    logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(del_downloaded_files, 'cron', day_of_week='mon-fri', hour=16,
                      minute=23)

    config = get_config()

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