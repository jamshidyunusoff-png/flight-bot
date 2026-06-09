"""
Keyboard definitions.
"""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

BTN_ADD_FLIGHT = "➕ Add Flight"
BTN_THIS_MONTH = "📅 This Month"
BTN_PREV_MONTH = "📆 Previous Month"
BTN_DELETE_LAST = "🗑 Delete Last Flight"

BTN_CONFIRM_YES = "✅ Yes"
BTN_CONFIRM_NO = "❌ No"


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ADD_FLIGHT)],
            [KeyboardButton(text=BTN_THIS_MONTH), KeyboardButton(text=BTN_PREV_MONTH)],
            [KeyboardButton(text=BTN_DELETE_LAST)],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Choose an option…",
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def confirm_delete_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=BTN_CONFIRM_YES, callback_data="delete_yes"),
                InlineKeyboardButton(text=BTN_CONFIRM_NO, callback_data="delete_no"),
            ]
        ]
    )
