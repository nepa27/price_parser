from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    ContentType,
    FSInputFile,
    Message,
    ReplyKeyboardRemove,
)

from keybords.for_questions import main_menu_kb, shops_kb


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        'Привет, я буду следить '
        'за ценами на Ваши товары!',
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == 'add_thing')
async def add_thing(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        'Выберите магазин',
        reply_markup=shops_kb(),
    )