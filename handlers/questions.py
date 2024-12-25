from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message,
)

from keybords.for_questions import (
    main_menu_kb,
    shops_kb,
    button_back_kb
)


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


@router.callback_query(F.data.startswith('shop'))
async def add_url(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    if callback.data.endswith('wildberies'):
        await callback.message.answer(
            'Это wildberies!',
        )
    if callback.data.endswith('lime'):
        await callback.message.answer(
            'Это lime!',
        )
    if callback.data.endswith('golden_apple'):
        await callback.message.answer(
            'Это golden_apple!',
        )
    if callback.data.endswith('gorzdrav'):
        await callback.message.answer(
            'Это gorzdrav!',
        )
    await callback.message.answer(
        'Вставьте ссылку на товар',
        reply_markup=button_back_kb(),
    )

