from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
)
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import validators

from db.db import add_data_on_thing, add_user, check_thing, get_list_things, get_one_thing, delete_one_thing
from keybords.for_questions import (
    main_menu_kb,
    button_back_kb
)
from log_config import logger
from utils.main import choose_shop


class AppStates(StatesGroup):
    main_menu = State()
    add_thing = State()
    my_tracking = State()
    thing = State()


router = Router()
cashed_user = set()


@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext, delete_previous: bool = False):
    user_id = message.from_user.id
    if user_id not in cashed_user:
        await add_user(user_id)
        cashed_user.add(user_id)
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


@router.message(AppStates.add_thing)
async def manipulation_with_url(message: Message, state: FSMContext):
    url = message.text
    user_id = message.from_user.id
    if validators.url(message.text):
        check_data = await check_thing(url, message.from_user.id)
        if check_data:
            await message.answer(
                'Товар уже находится в списке отслеживания!'
            )
        else:
            await message.answer(
                'Начинаем добавлять Ваш товар ...\n'
                'Это может занять несколько минут.'
            )
            data = await choose_shop(url)
            if data:
                await add_data_on_thing(url, user_id, data)
                await message.answer(
                    f'Товар "{data[0]}"\nдобавлен в Ваш список отслеживаний!'
                )
                logger.info(f'Товар "{data[0]}"\nдобавлен в Ваш список '
                            'отслеживаний!')
            else:
                await message.answer(
                    'Магазин недоступен!'
                )
        await cmd_start(message, state)
    else:
        await message.answer(
            'Это не url!\nВставьте корректную ссылку!'
        )


@router.callback_query(F.data == 'back')
async def go_to_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AppStates.add_thing:
        await state.set_state(AppStates.main_menu)
        await cmd_start(callback.message, state, delete_previous=True)
    if current_state == AppStates.my_tracking:
        await state.set_state(AppStates.main_menu)
        await cmd_start(callback.message, state, delete_previous=True)
    if current_state == AppStates.thing:
        await state.set_state(AppStates.my_tracking)
        await my_tracking(callback, state)

    await callback.answer()


@router.callback_query(F.data == 'my_tracking')
async def my_tracking(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppStates.my_tracking)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()

    builder = InlineKeyboardBuilder()
    user_id = callback.from_user.id

    data = await get_list_things(user_id)
    if data:
        for item in data:
            builder.add(InlineKeyboardButton(
                text=item.thing_name,
                callback_data=f'thing_{item.id}')
            )
        builder.add(InlineKeyboardButton(
            text='Назад',
            callback_data='back'
        ))
        builder.adjust(1)
        await callback.message.answer('Ваши отслеживания',
                                      reply_markup=builder.as_markup()
                                      )
    else:
        await callback.message.answer('Отслеживания отсутствуют!',
                                      reply_markup=button_back_kb(),
                                      )


@router.callback_query(F.data.startswith('thing_'))
async def thing(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AppStates.thing)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()

    think_id = callback.data.split('_')[1]
    data_thing = await get_one_thing(int(think_id))

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Удалить из списка',
        callback_data=f'delete_thing_{think_id}')
    )
    builder.add(InlineKeyboardButton(
        text='Назад',
        callback_data='back'
    ))
    builder.adjust(1)

    await callback.message.answer(
        f'<b>Название</b>: {data_thing.thing_name}\n'
        f'<b>Cсылка</b>: {data_thing.url}\n'
        f'<b>Дата добавления</b>: {data_thing.added_at}\n'
        f'<b>Цена</b>: {data_thing.latest_price.price}\n',
        reply_markup=builder.as_markup(),
        parse_mode='HTML'
    )


@router.callback_query(F.data.startswith('delete_thing_'))
async def delete_thing(callback: CallbackQuery, state: FSMContext):
    think_id = callback.data.split('_')[2]
    thing_name = await delete_one_thing(int(think_id))

    if thing_name:
        await callback.message.answer(
            f'Товар {thing_name} успешно удален!',
        )
        logger.info( f'Товар {thing_name} успешно удален!')
    else:
        await callback.message.answer(
            'Проблема при удалении товара, обратитесь в поддержку!',
        )
        logger.info(f'Проблема при удалении товара {think_id} - {thing_name},'
                    ' обратитесь в поддержку!')
    await state.set_state(AppStates.my_tracking)
    await my_tracking(callback, state)