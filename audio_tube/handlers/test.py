from aiogram import html, types, Router
from aiogram.utils.i18n import gettext as _ , I18nMiddleware
from aiogram.filters import Command
from fluentogram import TranslatorRunner

router = Router()


@router.message(Command("hello"))
async def handler(message: types.Message, i18n: TranslatorRunner):
    await message.answer(i18n.hello(name=message.from_user.username))