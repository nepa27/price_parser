from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
)
import validators

from keybords.for_questions import (
    main_menu_kb,
    shops_kb,
    button_back_kb
)


class AppStates(StatesGroup):
    main_menu = State()
    choose_shop = State()
    shop = State()


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext, delete_previous: bool = False):
    if delete_previous:
        await message.edit_reply_markup(reply_markup=None)
        await message.delete()
    await state.set_state(AppStates.main_menu)
    await message.answer(
        'Привет, я буду следить '
        'за ценами на Ваши товары!',
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == 'add_thing')
async def add_thing(callback: CallbackQuery, state: FSMContext, delete_previous: bool = False):
    await state.set_state(AppStates.choose_shop)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    await callback.message.answer(
        'Выберите магазин',
        reply_markup=shops_kb(),
    )


@router.callback_query(F.data.startswith('shop'))
async def add_url(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppStates.shop)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    # if callback.data.endswith('wildberies'):
    #     await callback.message.answer(
    #         'Это wildberies!',
    #     )
    # if callback.data.endswith('lime'):
    #     await callback.message.answer(
    #         'Это lime!',
    #     )
    # if callback.data.endswith('golden_apple'):
    #     await callback.message.answer(
    #         'Это golden_apple!',
    #     )
    # if callback.data.endswith('gorzdrav'):
    #     await callback.message.answer(
    #         'Это gorzdrav!',
    #     )
    await callback.message.answer(
        'Вставьте ссылку на товар',
        reply_markup=button_back_kb(),
    )


@router.callback_query(F.data == 'back')
async def go_to_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AppStates.choose_shop:
        current_state = await state.set_state(AppStates.main_menu)
        await cmd_start(callback.message, state, delete_previous=True)
    elif current_state == AppStates.shop:
        current_state = await state.set_state(AppStates.choose_shop)
        await add_thing(callback, state)

    await callback.answer()


@router.message(AppStates.shop)
async def manipulation_with_url(message: Message, state: FSMContext):
    if validators.url(message.text):
        await message.answer(
            'Валидный url!'
        )
        await cmd_start(message, state)
    else:
        await message.answer(
            'Это не url!'
        )
