from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from models import db_session
from service import db_service
from config import get_bot_config
from fluentogram import TranslatorRunner
import logging

router = Router()
config = get_bot_config()


@router.message(Command("start"))
async def cmd_start(message: types.Message, i18n: TranslatorRunner) -> None:
    lang = "ru" if message.from_user.language_code == "ru" else "en"
    await message.answer(text=i18n.start.text())

    # Добавление нового пользователя в базу данных
    session = db_session.create_session()
    if not db_service.is_user_already_created(telegram_id=message.from_user.id,
                                              session=session):
        user = db_service.create_user(telegram_id=message.from_user.id, session=session,
                                      lang=lang)
        settings = db_service.create_user_settings(user_id=user.id, session=session)
        logging.info(f"Created new user: telegram id - {user.telegram_id}")


@router.message(Command("help"))
async def cmd_help(message: types.Message, i18n: TranslatorRunner) -> None:
    await message.answer(text=i18n.help.text())


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext,
                     i18n: TranslatorRunner) -> None:
    await message.answer(
        text=i18n.cancel.text(),
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(Command("get_admin_statistic"), F.from_user.id == config.admin_id)
async def cmd_get_admin_statistic(message: types.Message, i18n: TranslatorRunner) -> None:
    session = db_session.create_session()

    statistic_text = i18n.admin.statistic.text(
        all_users=db_service.get_all_users_count(session),
        last_day_users=db_service.get_count_of_active_users_per_days(session, 1),
        last_week_users=db_service.get_count_of_active_users_per_days(session, 7),
        last_month_users=db_service.get_count_of_active_users_per_days(session, 30),
        all_podcasts=db_service.get_total_count_of_downloaded_podcasts(session)
    )

    await message.answer(text=statistic_text)
