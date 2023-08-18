from aiogram import Bot, Dispatcher
from handlers import dl_podcast, menu, base_cmd, test
from config import get_bot_config
from models import db_session
from service import set_bot_commands
from aiogram.utils.i18n import I18nMiddleware, I18n
from fluentogram import FluentTranslator, TranslatorHub
from fluent_compiler.bundle import FluentBundle
from middlewares.translator import TranslatorRunnerMiddleware
import asyncio
import logging


async def main():
    logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG)
    db_session.global_init("db/database.db")

    config = get_bot_config()

    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en",)
        },
        [
            FluentTranslator(
                locale="en", 
                translator=FluentBundle.from_files("en-US", filenames=["./locales/en.ftl"])
            ),
            FluentTranslator(
                locale="ru", 
                translator=FluentBundle.from_files("ru", filenames=["./locales/ru.ftl"])
            )
        ],
    )


    bot = Bot(token=config.bot_token, parse_mode="HTML")
    await set_bot_commands(bot)

    dp = Dispatcher()
    dp.message.middleware(TranslatorRunnerMiddleware())

    dp.include_routers(
        test.router, base_cmd.router, menu.router, dl_podcast.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Программа завершена")
