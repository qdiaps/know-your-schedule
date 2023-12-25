from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data import paths, text
from data.json_tools import deserialization
from data.schedule_tools import default_days
from utils import group_utils
from utils.states import Show
from keyboards import reply, builders

router = Router()


async def process_data(state: FSMContext, data: dict) -> InlineKeyboardBuilder:
    names = tuple(data.keys())
    names_into_groups = group_utils.split_into_groups(names, 5)
    builder = builders.create_page_with_navigation(names_into_groups[0])
    await state.update_data(current_page=0)
    await state.update_data(pages_obj=names_into_groups)
    return builder


@router.message(StateFilter(None), F.text.lower() == 'показати')
async def selection_school_handler(message: Message, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    if not schedules.keys():
        await message.answer(text=f'{text.warning_is_not_schools}', reply_markup=reply.main)
    else:
        builder = await process_data(state, schedules)
        await state.set_state(Show.school_name)
        await message.answer(text=f'{text.info_how_to_navigation}', reply_markup=reply.exit_state)
        await message.answer(text='<b><i>Школи: </i></b>', reply_markup=builder.as_markup())


@router.message(Show.school_name, F.text)
async def message_handler(message: Message) -> None:
    await message.answer(text=f'{text.warning_is_not_command}')


@router.callback_query(Show.school_name, F.data)
async def selection_class_handler(callback: CallbackQuery, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    if not schedules[callback.data].keys():
        await callback.message.answer(text=f'{text.warning_is_not_classes}')
    else:
        builder = await process_data(state, schedules[callback.data])
        await state.update_data(school_name=callback.data)
        await state.set_state(Show.class_name)
        await callback.message.delete()
        await callback.message.answer(text='<b><i>Класи: </i></b>', reply_markup=builder.as_markup())
    await callback.answer()


@router.message(Show.class_name, F.text)
async def message_handler_class(message: Message) -> None:
    await message.answer(text=f'{text.warning_is_not_command}')


@router.callback_query(Show.class_name, F.data)
async def confirm_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    output_text = f'<b><i>Школа: </i></b>{data["school_name"]}<b><i>, клас: </i></b>{callback.data}.'
    await state.update_data(class_name=callback.data)
    await state.set_state(Show.confirm)
    await callback.message.delete()
    await callback.message.answer(text=f'<b><i>Все вірно? </i></b>{output_text}', reply_markup=reply.yes_or_no)
    await callback.answer()


@router.message(Show.confirm, F.text)
async def confirm_message_handler(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    schedules = deserialization(paths.schedules)
    if msg == 'так':
        data = await state.get_data()
        schedules = schedules[data['school_name']][data['class_name']]
        output_text = f'<b><i>{default_days[0]}:</i></b>\n'
        builder = builders.create_page_with_navigation(schedules[default_days[0]])
        await state.update_data(current_page=0)
        await state.update_data(pages_obj=schedules)
        await state.update_data(can_edit_text='yes')
        await state.set_state(Show.show_schedule)
        await message.answer(text=f'{text.warning_if_not_schedules}', reply_markup=reply.exit_state)
        await message.answer(text=f'{output_text}', reply_markup=builder.as_markup())
    elif msg == 'ні':
        builder = await process_data(state, schedules)
        await state.set_state(Show.school_name)
        await message.answer(text='<b><i>Вибери школу:</i></b>', reply_markup=builder.as_markup())
    else:
        await message.answer(text=f'{text.warning_is_not_command}')
