from aiogram import Router, types, F
from aiogram.filters import Command, Filter
import config
from service import db_service
from models import db_session
from fluentogram import TranslatorRunner

router = Router()
bot_config = config.get_bot_config()

class AdminFilter(Filter):
    def __init__(self, cfg: config.Config) -> None:
        self.bot_config = cfg

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in self.bot_config.allowed_list


@router.message(Command("del_diff_download"), AdminFilter(bot_config))
async def cmd_set_diff_download(message: types.Message, i18n: TranslatorRunner) -> None:
    db_service.update_min_diff_download(
        telegram_id=message.from_user.id,
        session=db_session.create_session(),
        new_value=0
    )
    await message.answer(text=i18n.del_diff.text(new_value="0"))



@router.message(Command("add_admin"), AdminFilter(bot_config))
async def cmd_set_diff_download(message: types.Message, i18n: TranslatorRunner) -> None:
    tokens = message.text.split()
    if len(tokens) < 2 or (not tokens[1].isdigit()):
        return
    new_admin: int = int(tokens[1])
    db_service.update_min_diff_download(
        telegram_id=new_admin,
        session=db_session.create_session(),
        new_value=0
    )
    bot_config.allowed_list.append(new_admin)    
    await message.answer(text=i18n.add_new_admin.text())
    
