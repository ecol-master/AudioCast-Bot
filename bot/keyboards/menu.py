from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from fluentogram import TranslatorRunner

class MenuCallback(CallbackData, prefix="menu"):
    action: str
    stage: int

# Menu Settings
#
def get_menu_kb(i18n: TranslatorRunner) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=i18n.button_settings.text(), callback_data=MenuCallback(action="settings", stage=1).pack()),
        types.InlineKeyboardButton(text=i18n.button_languages.text(), callback_data=MenuCallback(action="languages", stage=1).pack())
    )
    return builder.as_markup()

#
def get_settings_kb(i18n: TranslatorRunner) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.button_caption_length.text(), 
            callback_data=MenuCallback(action="caption_length", stage=2).pack()
        ),
        types.InlineKeyboardButton(
            text=i18n.button_del_link.text(), 
            callback_data=MenuCallback(action="del_link", stage=2).pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(text=i18n.button_back.text(), callback_data=MenuCallback(action="back", stage=2).pack())
    )
    return builder.as_markup()


#
def get_settings_del_link_kb(i18n: TranslatorRunner) -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text=i18n.button_del_link_yes.text()),
            types.KeyboardButton(text=i18n.button_del_link_no.text())
        ]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=i18n.button_del_link_placeholder.text()
    )

# Menu Languages

def get_languages_kb(i18n: TranslatorRunner) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data=MenuCallback(action="choose_ru_lang", stage=2).pack()),
        types.InlineKeyboardButton(text="🇬🇧 English", callback_data=MenuCallback(action="choose_en_lang", stage=2).pack())
    )
    builder.row(
        types.InlineKeyboardButton(text=i18n.button_back.text(), callback_data=MenuCallback(action="back", stage=2).pack())
    )
    return builder.as_markup()
