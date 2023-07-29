from aiogram import Router, types, Bot
from aiogram.filters import Command
from podcast import make_podcast, CantDownloadAudioError
from utils import get_message_url
from utils import message_texts
from config import on_delete_filenames
import logging

router = Router()


@router.message(Command("start"))
async def cmd_message(message: types.Message):
    await message.answer(text=message_texts.GREETINGS)


@router.message()
async def process_send_url(message: types.Message, bot: Bot):
    urls = get_message_url(message)
    if not urls:
        await message.answer(text="В вашем сообщении нету ссылки на видео.")
        return

    load_message = await message.answer(text="Downloading...🕔")
    try:
        podcast = make_podcast(urls[0])
        await bot.send_audio(chat_id=message.chat.id, **podcast.__dict__)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        # on_delete_filenames.append(podcast.filename)

    except CantDownloadAudioError:
        await message.answer(text="Check your video url!")
        return
    except Exception as _err:
        logging.error(f"{_err}")
    finally:
        await bot.delete_message(chat_id=load_message.chat.id,
                                 message_id=load_message.message_id)
