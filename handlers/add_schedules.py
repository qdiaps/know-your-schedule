import re

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Add
from keyboards import reply
from data.json_tools import deserialization, serialization
from data import paths, schedule_tools, text

router = Router()
users_data = {}


@router.message(F.text.lower().in_(['додати']))
async def start_adding_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Add.school_name)
    await message.answer(text=f'{text.get_shool_name}', reply_markup=reply.exit_state)


@router.message(Add.school_name, F.text)
async def add_school_handler(message: Message, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    if message.text not in schedules.keys():
        if '\n' in message.text:
            await message.answer(text=f'{text.warning_check_to_line_break}')
            return
        schedule_tools.add_new_school(message.text, schedules)
        serialization(schedules, paths.schedules)
        await message.answer(text=f'{text.school_added}', reply_markup=reply.yes_or_no)
    else:
        await message.answer(text=f'{text.school_was_adding}', reply_markup=reply.yes_or_no)
    await state.update_data(school_name=message.text)
    await state.set_state(Add.confirm_school_name)


@router.message(Add.confirm_school_name, F.text)
async def confirm_school_name(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'так':
        await state.set_state(Add.class_name)
        await message.answer(text=f'{text.get_class_name}', reply_markup=reply.exit_state)
    elif msg == 'ні':
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')


@router.message(Add.class_name, F.text)
async def add_class_handler(message: Message, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    data = await state.get_data()
    if message.text not in schedules[data['school_name']].keys():
        if '\n' in message.text:
            await message.answer(text=f'{text.warning_check_to_line_break}')
            return
        schedule_tools.add_new_class(data['school_name'], message.text, schedules)
        serialization(schedules, paths.schedules)
        await message.answer(text=f'{text.class_added}', reply_markup=reply.yes_or_no)
    else:
        await message.answer(text=f'{text.class_was_adding}', reply_markup=reply.yes_or_no)
    await state.update_data(class_name=message.text)
    await state.set_state(Add.confirm_class_name)


@router.message(Add.confirm_class_name, F.text)
async def confirm_class_name(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'так':
        await state.set_state(Add.day)
        await message.answer(text=f'{text.get_day}', reply_markup=reply.days)
    elif msg == 'ні':
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')


@router.message(Add.day, F.text)
async def weekday_selection_handler(message: Message, state: FSMContext) -> None:
    msg = message.text
    if msg in schedule_tools.default_days:
        await state.update_data(day=msg)
        await state.set_state(Add.schedule)
        await message.answer(text=f'{text.get_schedules}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_this_day_is_not}', reply_markup=reply.days)


@router.message(Add.schedule, F.text)
async def add_schedules_handler(message: Message, state: FSMContext) -> None:
    if '\n' in message.text:
        await message.answer(text=f'{text.warning_check_to_line_break}')
        return
    lessons = re.split(',', message.text)
    lessons = [lesson.lstrip() for lesson in lessons]
    for i in range(0, len(lessons)):
        lessons[i] = f'{i + 1}. {lessons[i]}'
    name_lessons = ''
    for lesson in lessons:
        name_lessons += f'{lesson}\n'
    await state.update_data(schedules=lessons)
    await state.set_state(Add.confirm_schedules)
    await message.answer(text=f'<b><i>Ось що вийшло: \n{name_lessons}Все вірно?</i></b>', reply_markup=reply.yes_or_no)


@router.message(Add.confirm_schedules, F.text)
async def confirm_schedules(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'так':
        data = await state.get_data()
        school_name = data['school_name']
        class_name = data['class_name']
        day = data['day']
        lessons = data['schedules']
        schedules = deserialization(paths.schedules)
        schedule_tools.add_new_schedule(school_name, class_name, day, lessons, schedules)
        serialization(schedules, paths.schedules)
        await state.clear()
        await message.answer(text=f'{text.schedules_added}', reply_markup=reply.main)
    elif msg == 'ні':
        await state.set_state(Add.schedule)
        await message.answer(text=f'{text.input_schedules_again}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_is_not_command}', reply_markup=reply.yes_or_no)
