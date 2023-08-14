from aiogram import Router, types, Bot
from aiogram.filters import Command
from podcast import get_podcast
from service import message_texts, get_message_urls, rm_downloaded_files, \
    CantDownloadAudioError, DurationLimitError
from models import db_session

from service import db_service
import logging

router = Router()


@router.message(Command("start"))
async def cmd_message(message: types.Message):
    session = db_session.create_session()
    if not db_service.user_is_already_created(telegram_id=message.from_user.id,
                                              session=session):
        user = db_service.create_user(telegram_id=message.from_user.id, session=session)
        settings = db_service.create_user_settings(user_id=user.id, session=session)
        print(user.settings, settings)
        logging.info(f"Created new user: telegram id - {user.telegram_id}")
    await message.answer(text=message_texts.GREETINGS)


@router.message()
async def process_send_url(message: types.Message, bot: Bot):
    urls = get_message_urls(message)
    if not urls:
        await message.answer(text="В вашем сообщении нету ссылки на видео.")
        return

    load_message = await message.answer(text="Downloading...🕔")
    try:
        session = db_session.create_session()
        user_settings = db_service.get_user_settings(telegram_id=message.from_user.id,
                                                     session=session)
        podcast = get_podcast(urls[0], settings=user_settings)
        await bot.send_audio(chat_id=message.chat.id, **podcast.as_dict())
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await rm_downloaded_files(podcast.filename)

    except CantDownloadAudioError:
        await message.answer(text="Check your video url!")

    except DurationLimitError:
        await message.answer(text="This podcast is too long.")

    except Exception as _err:
        logging.error(f"{_err}")
    finally:
        await bot.delete_message(chat_id=load_message.chat.id,
                                 message_id=load_message.message_id)
