from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Мои отслеживания',
        callback_data='my_tracking'
    )
    kb.button(
        text='Добавить товар',
        callback_data='add_thing'
    )
    kb.button(
        text='Сообщить об ошибке',
        callback_data='send_message'
    )
    kb.button(
        text='Поддержать проект',
        callback_data='donate'
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def shops_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Wildberies',
        callback_data='wildberies'
    )
    kb.button(
        text='Lime',
        callback_data='lime'
    )
    kb.button(
        text='Золотое яблоко',
        callback_data='golden_apple'
    )
    kb.button(
        text='Аптека Горздрав',
        callback_data='gorzdrav'
    )
    kb.button(
        text='Назад',
        callback_data='back'
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
