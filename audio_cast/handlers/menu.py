from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from audio_cast.keyboards import MenuCallback, get_menu_kb, get_settings_kb, \
            get_settings_del_link_kb, get_languages_kb
from audio_cast.models import db_session
from audio_cast.service import db_service, validate_new_caption_length, \
    validate_answer_del_link
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner


router = Router()

@router.message(Command("menu"))
async def cmd_menu(message: types.Message, i18n: TranslatorRunner):
    kb = get_menu_kb(i18n)
    await message.answer(text=i18n.menu.main.text(), reply_markup=kb)

# SETTINGS BUTTON
@router.callback_query(MenuCallback.filter(F.action == "settings"))
async def menu_callback_settings(query: types.CallbackQuery, bot: Bot, i18n: TranslatorRunner) -> None:
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=get_settings_kb(i18n)
    )


# menu callback: caption_length

class SetNewCaptionLength(StatesGroup):
    new_length = State()

@router.callback_query(MenuCallback.filter(F.action == "caption_length"))
async def menu_caption_length(query: types.CallbackQuery, bot: Bot, state: FSMContext, 
                              i18n: TranslatorRunner) -> None:
    await query.answer()
    session = db_session.create_session()
    current_caption_length = db_service.get_settings_caption(
        telegram_id=query.from_user.id, session=session
    )
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=i18n.menu.set_caption.text(current_length=current_caption_length)
    )
   
    await state.set_state(SetNewCaptionLength.new_length)
    await state.update_data({
        "current_length": current_caption_length
    })


@router.message(SetNewCaptionLength.new_length)
async def process_set_new_value(message: types.Message, state: FSMContext, 
                                i18n: TranslatorRunner) -> None:
    try:
        new_length = validate_new_caption_length(message.text.strip())
        session = db_session.create_session()
        updated_settings = db_service.update_settings_caption(
            telegram_id=message.from_user.id, session=session, new_length=new_length
        )
        await message.answer(text=i18n.menu.set_caption_success.text(new_length=new_length))
        await state.clear()
    except ValueError:
        state_data = await state.get_data()
        current_length = state_data["current_length"]
        await message.answer(text=i18n.menu.set_caption_error.text(current_length=current_length))


# menu callback: del_link

class ChangeIsDeleteLink(StatesGroup):
    is_delete = State()


@router.callback_query(MenuCallback.filter(F.action == "del_link"))
async def menu_del_link(query: types.CallbackQuery, bot: Bot, state: FSMContext,
                        i18n: TranslatorRunner) -> None:
    await query.answer()

    await bot.send_message(
        chat_id=query.message.chat.id,
        text=i18n.menu.set_is_del_link.text(), 
        reply_markup=get_settings_del_link_kb(i18n),
    )

    await state.set_state(ChangeIsDeleteLink.is_delete)

@router.message(ChangeIsDeleteLink.is_delete)
async def process_menu_del_link(message: types.Message, state: FSMContext,
                                i18n: TranslatorRunner, bot: Bot,) -> None:
    try:
        result = validate_answer_del_link(ans=message.text)
        if result:
            await message.answer(
                text=i18n.menu.is_del_link_true.text(), 
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                text=i18n.menu.is_del_link_false.text(),
                reply_markup=types.ReplyKeyboardRemove()
            )
        session = db_session.create_session()
        db_service.update_setting_is_del_link(
            telegram_id=message.from_user.id, session=session, is_del_link=result
        )
        await state.clear()
        
    except ValueError:
        await message.answer(
            text=i18n.menu.set_is_del_link_error.text(),
            reply_markup=get_settings_del_link_kb(i18n)
            )

# menu callback: back

@router.callback_query(MenuCallback.filter((F.action == "back") & (F.stage == 2)))
async def menu_back(query: types.CallbackQuery, bot: Bot, i18n: TranslatorRunner) -> None:
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=get_menu_kb(i18n)
    )
    await query.answer(text=i18n.menu.back_query_answer.text())


# LANGUAGES BUTTON
@router.callback_query(MenuCallback.filter(F.action == "languages"))
async def menu_languages(query: types.CallbackQuery, bot: Bot, i18n: TranslatorRunner) -> None:
    await query.answer()
    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=i18n.menu.choose_language.text(),
        reply_markup=get_languages_kb(i18n)
    )


@router.callback_query(MenuCallback.filter(F.action == "choose_ru_lang"))
async def menu_language_russian(query: types.CallbackQuery, bot: Bot,
                                i18n: TranslatorRunner) -> None:
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=i18n.menu.choose_ru_lang_query_answer.text()
    )
    await query.answer()    

    session = db_session.create_session()
    db_service.update_lang(telegram_id=query.from_user.id, session=session, new_lang="ru")

@router.callback_query(MenuCallback.filter(F.action == "choose_en_lang"))
async def menu_language_english(query: types.CallbackQuery, bot: Bot,
                                i18n: TranslatorRunner) -> None:
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=i18n.menu.choose_en_lang_query_answer.text()
    )
    await query.answer()
    

    session = db_session.create_session()
    db_service.update_lang(telegram_id=query.from_user.id, session=session, new_lang="en")

