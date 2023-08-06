from aiogram import Router, types, Bot
from aiogram.filters import Command
from podcast import PodcastMaker, CantDownloadAudioError, DurationLimitError
from service import message_texts, get_message_urls, rm_downloaded_files
import logging

router = Router()


@router.message(Command("start"))
async def cmd_message(message: types.Message):
    await message.answer(text=message_texts.GREETINGS)


@router.message()
async def process_send_url(message: types.Message, bot: Bot):
    urls = get_message_urls(message)
    if not urls:
        await message.answer(text="В вашем сообщении нету ссылки на видео.")
        return

    load_message = await message.answer(text="Downloading...🕔")
    try:
        maker = PodcastMaker(url=urls[0])
        podcast = maker.get_podcast_data()
        await maker.download()

        await bot.send_audio(chat_id=message.chat.id, **podcast.__dict__)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await rm_downloaded_files(maker.filename)
    except CantDownloadAudioError:
        await message.answer(text="Check your video url!")
    except DurationLimitError:
        await message.answer(text="This podcast is too long.")
    except Exception as _err:
        logging.error(f"{_err}")
    finally:
        await bot.delete_message(chat_id=load_message.chat.id,
                                 message_id=load_message.message_id)
