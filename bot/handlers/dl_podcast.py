from aiogram import types, Bot, Router
from bot.service import get_message_urls, db_service, CantDownloadAudioError, \
    DurationLimitError, rm_downloaded_files
from bot.models import db_session
from bot.models.user_settings import UserSettings
from sqlalchemy.orm import Session
from bot.podcast import get_podcast
from fluentogram import TranslatorRunner
import logging

router = Router()


def can_download(event):
    async def wrapper(message: types.Message, bot: Bot, i18n: TranslatorRunner):
        urls = get_message_urls(message)
        if not urls:
            await message.answer(text=i18n.no_url_in_message.text())
            return

        session = db_session.create_session()
        if db_service.is_can_download_podcast(telegram_id=message.from_user.id,
                                              session=session):
            await event(message, bot, session, urls[0], i18n)

            db_service.update_count_of_downloaded_podcast(
                telegram_id=message.from_user.id, session=session)

            db_service.update_date_last_podcast_download(
                telegram_id=message.from_user.id, session=session)
        else:
            await message.answer(text=i18n.dowload_podcast_is_no_ability.text())

    return wrapper


@router.message()
@can_download
async def process_podcast_download(message: types.Message, bot: Bot, session: Session,
                                   url: str, i18n: TranslatorRunner):
    load_message = await message.answer(text=i18n.load_message.text())
    try:
        user_settings: UserSettings = db_service.get_user_settings(
            telegram_id=message.from_user.id,
            session=session)
        podcast = get_podcast(url, settings=user_settings)
        await bot.send_audio(chat_id=message.chat.id, **podcast.as_dict())

        if user_settings.is_del_link:
            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=message.message_id)

        await rm_downloaded_files(podcast.title)

    except CantDownloadAudioError:
        await message.answer(text=i18n.download_audio_error.text())

    except DurationLimitError:
        await message.answer(text=i18n.duration_limit_error.text())

    except Exception as _err:
        logging.error(f"Error: {_err}")
    finally:
        await bot.delete_message(chat_id=load_message.chat.id,
                                 message_id=load_message.message_id)
