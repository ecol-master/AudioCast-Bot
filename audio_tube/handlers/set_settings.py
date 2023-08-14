from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from service import message_texts
from aiogram.fsm.state import State, StatesGroup
from service import db_service
from models import db_session


class SetNewCaptionLength(StatesGroup):
    new_length = State()


router = Router()


@router.message(Command("set_caption"))
async def cmd_set_caption(message: types.Message, state: FSMContext):
    session = db_session.create_session()
    current_caption_length = db_service.get_settings_caption(
        telegram_id=message.from_user.id, session=session
    )
    await message.answer(
        text=message_texts.SET_CAPTION_TEXT.format(current_caption_length)
    )
    await state.set_state(SetNewCaptionLength.new_length)
    await state.update_data({
        "current_length": current_caption_length
    })


@router.message(SetNewCaptionLength.new_length)
async def process_set_new_value(message: types.Message, state: FSMContext):
    try:
        new_length = validate_new_caption_length(message.text.strip())
        session = db_session.create_session()
        updated_settings = db_service.update_settings_caption(
            telegram_id=message.from_user.id, session=session, new_length=new_length
        )
        await message.answer(text=message_texts.SET_CAPTION_TEXT_SUCCESS.format(
            updated_settings.caption_length)
        )
        await state.clear()
    except ValueError:
        state_data = await state.get_data()
        current_length = state_data["current_length"]
        await message.answer(
            text=message_texts.SET_CAPTION_TEXT_ERROR.format(current_length))


def validate_new_caption_length(new_length: str) -> int:
    if not new_length.isdecimal() or not new_length:
        raise ValueError
    new_length = int(new_length)
    return 150 if new_length > 150 else new_length
