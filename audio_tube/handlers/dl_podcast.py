from aiogram import types, Bot, Router
from service import get_message_urls, db_service, message_texts, \
    CantDownloadAudioError, DurationLimitError, rm_downloaded_files
from models import db_session
from models.user_settings import UserSettings
from sqlalchemy.orm import Session
from podcast import get_podcast
import logging


router = Router()


def can_download(func):
    async def wrapper(message: types.Message, bot: Bot):
        urls = get_message_urls(message)
        if not urls:
            await message.answer(text="В вашем сообщении нету ссылки на видео.")
            return

        session = db_session.create_session()
        if db_service.is_can_download_podcast(telegram_id=message.from_user.id,
                                              session=session):
            await func(message, bot, session, urls[0])

            # Обновляю количество скачанных подкастов пользователем
            db_service.update_count_of_downloaded_podcast(
                telegram_id=message.from_user.id, session=session)
            # Ставлю новое время начала загрузки
            db_service.update_date_last_podcast_download(
                telegram_id=message.from_user.id, session=session)
        else:
            await message.answer(text=message_texts.DOWNLOAD_PODCAST_IS_NO_ABILITY)

    return wrapper


@router.message()
@can_download
async def process_podcast_download(message: types.Message, bot: Bot, session: Session,
                                   url: str):
    load_message = await message.answer(text="Downloading...🕔")
    try:
        user_settings: UserSettings = db_service.get_user_settings(telegram_id=message.from_user.id,
                                                     session=session)
        podcast = get_podcast(url, settings=user_settings)
        await bot.send_audio(chat_id=message.chat.id, **podcast.as_dict())
        
        if user_settings.is_del_link:
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
