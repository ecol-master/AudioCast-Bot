from aiogram import types, Router, F
from aiogram.filters import Command
from service import db_service, message_texts
from models import db_session
from config import get_bot_config

router = Router()
config = get_bot_config()


@router.message(Command("get_admin_statistic"), F.from_user.id == config.admin_id)
async def cmd_get_admin_statistic(message: types.Message) -> None:
    session = db_session.create_session()
    await message.answer(text=message_texts.ADMIN_STATISTIC_TEXT.format(
        db_service.get_all_users_count(session),
        db_service.get_count_of_active_users_per_days(session, 1),
        db_service.get_count_of_active_users_per_days(session, 7),
        db_service.get_count_of_active_users_per_days(session, 30),
        db_service.get_total_count_of_downloaded_podcasts(session)
    ))
