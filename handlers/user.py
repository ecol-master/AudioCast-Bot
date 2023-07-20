from aiogram import Router, types, Bot
from aiogram.filters import Command
from podcast.make_podcast import make_podcast
from utils import get_message_url
from podcast.exceptions import CantDownloadVideoError
from utils import message_texts

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
    try:
        podcast = make_podcast(urls[0])
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=podcast.audio,
            caption=podcast.caption,
            title=podcast.title,
            performer=podcast.performer,
            duration=podcast.duration,
            thumb=podcast.thumb
        )
    except CantDownloadVideoError:
        await message.answer(text="Check your video url!")
    except Exception as _err:
        print("FUNC", _err)
