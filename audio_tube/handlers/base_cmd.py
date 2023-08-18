from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from service import message_texts
from models import db_session
from service import db_service
from config import get_bot_config
import logging

router = Router()
config = get_bot_config()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    lang = "ru" if message.from_user.language_code == "ru" else "en"
    await message.answer(text=message_texts.GREETINGS)

    # Добавление нового пользователя в базу данных
    session = db_session.create_session()
    if not db_service.is_user_already_created(telegram_id=message.from_user.id,
                                              session=session):
        user = db_service.create_user(telegram_id=message.from_user.id, session=session, lang=lang)
        settings = db_service.create_user_settings(user_id=user.id, session=session)
        logging.info(f"Created new user: telegram id - {user.telegram_id}")


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    await message.answer(text=message_texts.CMD_HELP_TEXT)


@router.message(Command("cancel"))
async def cmd_cansel(message: types.Message, state: FSMContext) -> None:
    await message.answer(text="Последнее действие отменено.")
    await state.clear()

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