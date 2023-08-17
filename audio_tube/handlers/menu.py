from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from keyboards import MenuCallback, get_menu_kb, get_settings_kb, \
            get_settings_del_link_kb
from models import db_session
from service import db_service, message_texts, validate_new_caption_length, \
    validate_answer_del_link
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router = Router()

@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    kb = get_menu_kb()
    await message.answer(text="Выберите команду из списка ниже", reply_markup=kb)

# SETTINGS BUTTON

@router.callback_query(MenuCallback.filter(F.action == "settings"))
async def menu_callback_settings(query: types.CallbackQuery, bot: Bot, 
                                callback_data: MenuCallback) -> None:
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=get_settings_kb()
    )


# menu callback: caption_length

class SetNewCaptionLength(StatesGroup):
    new_length = State()

@router.callback_query(MenuCallback.filter(F.action == "caption_length"))
async def menu_caption_length(query: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await query.answer()
    session = db_session.create_session()
    current_caption_length = db_service.get_settings_caption(
        telegram_id=query.from_user.id, session=session
    )
    await bot.send_message(
        chat_id=query.message.chat.id,
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


# menu callback: del_link

class ChangeIsDeleteLink(StatesGroup):
    is_delete = State()


@router.callback_query(MenuCallback.filter(F.action == "del_link"))
async def menu_del_link(query: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await query.answer()

    await bot.send_message(
        chat_id=query.message.chat.id,
        text=message_texts.SET_IS_DELETE_LINK, 
        reply_markup=get_settings_del_link_kb()
    )

    await state.set_state(ChangeIsDeleteLink.is_delete)

@router.message(ChangeIsDeleteLink.is_delete)
async def process_menu_del_link(message: types.Message, state: FSMContext) -> None:
    try:
        result = validate_answer_del_link(ans=message.text)
        if result:
            await message.answer(text="Теперь ссылка будет удаляться автоматически.")
        else:
            await message.answer(text="Теперь ссылку не будет удаляться автоматически.")
        session = db_session.create_session()
        db_service.update_setting_is_del_link(
            telegram_id=message.from_user.id, session=session, is_del_link=result
        )
        await state.clear()
        
    except ValueError:
        await message.answer(
            text="Пожалуйста, отправьте сообщение с ответом (Да / Нет) или нажмите на кнопку ниже.",
            reply_markup=get_settings_del_link_kb()
            )

# menu callback: back

@router.callback_query(MenuCallback.filter(F.action == "back" and F.stage == 2))
async def menu_back(query: types.CallbackQuery, bot: Bot) -> None:
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=get_menu_kb()
    )
    await query.answer(text="Back")


# LANGUAGES BUTTON
