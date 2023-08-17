from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MenuCallback(CallbackData, prefix="menu"):
    action: str
    stage: int

#
def get_menu_kb() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Setting", callback_data=MenuCallback(action="settings", stage=1).pack()),
        types.InlineKeyboardButton(text="Languages", callback_data=MenuCallback(action="languages", stage=1).pack())
    )
    return builder.as_markup()

#
def get_settings_kb() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Caption Len", callback_data=MenuCallback(action="caption_length", stage=2).pack()),
        types.InlineKeyboardButton(text="Del Link", callback_data=MenuCallback(action="del_link", stage=2).pack())
    )
    builder.row(
        types.InlineKeyboardButton(text="<< Назад", callback_data=MenuCallback(action="back", stage=2).pack())
    )
    return builder.as_markup()


#
def get_settings_del_link_kb() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Ваш ответ"
    )