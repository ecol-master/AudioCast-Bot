from aiogram import Bot, Dispatcher
from handlers import dl_podcast, menu, base_cmd
from config import get_bot_config, DATABASE_FILE, LOG_FILE
from models import db_session
from service import set_bot_commands, get_translator_hub
from middlewares.translator import TranslatorRunnerMiddleware
import asyncio
import logging


async def main():
    logging.basicConfig(filename=LOG_FILE, filemode="w", level=logging.DEBUG)
    db_session.global_init(db_file=DATABASE_FILE)

    config = get_bot_config()

    bot = Bot(token=config.bot_token, parse_mode="HTML")
    await set_bot_commands(bot)

    dp = Dispatcher()
    dp.message.middleware(TranslatorRunnerMiddleware())
    dp.callback_query.middleware(TranslatorRunnerMiddleware())

    dp.include_routers(
        base_cmd.router, menu.router, dl_podcast.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, _translator_hub=get_translator_hub())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Программа завершена")
