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


def tracking_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Последние изменения',
        callback_data='last_changes'
    )
    kb.button(
        text='Статистика',
        callback_data='statistic'
    )
    kb.button(
        text='Уведомления',
        callback_data='notification'
    )
    kb.button(
        text='Удалить',
        callback_data='delete_thing'
    )
    kb.button(
        text='Назад',
        callback_data='back'
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def choose_notifications() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Каждые 3 часа',
        callback_data='every_third_hours_notification'
    )
    kb.button(
        text='Раз в сутки',
        callback_data='one_time_day_notification'
    )
    kb.button(
        text='При изменении цены',
        callback_data='price_change_notification'
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def button_back_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Назад',
        callback_data='back'
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def question_on_delete_thing_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Да',
        callback_data='yes_delete'
    )
    kb.button(
        text='Нет',
        callback_data='no_delete'
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
