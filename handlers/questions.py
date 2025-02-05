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
    button_back_kb
)
from utils.shops import golden_apple, lime, wb


class AppStates(StatesGroup):
    main_menu = State()
    add_thing = State()
    shop = State()


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext, delete_previous: bool = False):
    await state.set_state(AppStates.main_menu)
    if delete_previous:
        await message.edit_reply_markup(reply_markup=None)
        await message.delete()
    await message.answer(
        'Привет, я буду следить '
        'за ценами на Ваши товары!',
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == 'add_thing')
async def add_thing(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppStates.add_thing)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    await callback.message.answer(
        'Вставьте ссылку на товар\n'
        'Доступные магазины:\n'
        '- Wildberies\n'
        '- Lime\n'
        '- Золотое яблоко\n',
        reply_markup=button_back_kb(),
    )


@router.message(AppStates.shop)
async def manipulation_with_url(message: Message, state: FSMContext):
    if validators.url(message.text):
        # тут логика по парсингу цены товара
        # Передаем пользователю информацию о добавлении
        # товара и возвращаем его имя и цену
        data = None
        # Сделать в БД запрос на предмет существования этого товара у этого пользователя
        check_data = None
        if check_data:
            await message.answer(
                'Товар уже находится в списке отслеживания!'
                f'{data}'
            )
        else:
            await message.answer(
                'Товар добавлен в Ваш список отслеживаний!'
                f'{data}'
            )
        await cmd_start(message, state)
    else:
        await message.answer(
            'Это не url!'
        )


@router.callback_query(F.data == 'back')
async def go_to_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AppStates.add_thing:
        current_state = await state.set_state(AppStates.main_menu)
        await cmd_start(callback.message, state, delete_previous=True)

    await callback.answer()


