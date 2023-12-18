import re

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import user_tools
from utils.states import Add
from keyboards import reply
from data.json_tools import deserialization, serialization
from data import paths, schedule_tools, text

router = Router()
users_data = {}


@router.message(F.text.lower().in_(['додати']))
async def start_adding_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    if user_tools.is_user_in_state(message.from_user.id):
        return
    user_tools.set_user_in_state(message.from_user.id)
    await state.set_state(Add.school_name)
    await message.answer(text=f'{text.get_shool_name}', reply_markup=reply.exit_state)


@router.message(Add.school_name, F.text)
async def add_school_handler(message: Message, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    if message.text.lower() == 'вихід':
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
        return
    elif message.text not in schedules.keys():
        schedule_tools.add_new_school(message.text, schedules)
        serialization(schedules, paths.schedules)
        await message.answer(text=f'{text.school_added}', reply_markup=reply.yes_or_no)
    else:
        await message.answer(text=f'{text.school_was_adding}', reply_markup=reply.yes_or_no)
    users_data[message.from_user.id] = {}
    users_data[message.from_user.id]['school_name'] = message.text
    await state.set_state(Add.confirm_school_name)


@router.message(Add.confirm_school_name, F.text)
async def confirm_school_name(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'так':
        await state.set_state(Add.class_name)
        await message.answer(text=f'{text.get_class_name}', reply_markup=reply.exit_state)
    elif msg == 'ні' or msg == 'вихід':
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')


@router.message(Add.class_name, F.text)
async def add_class_handler(message: Message, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    data = await state.get_data()
    if message.text.lower() == 'вихід':
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
        return
    elif message.text not in schedules[users_data[message.from_user.id]['school_name']].keys():
        schedule_tools.add_new_class(
            users_data[message.from_user.id]['school_name'], message.text, schedules)
        serialization(schedules, paths.schedules)
        await message.answer(text=f'{text.class_added}', reply_markup=reply.yes_or_no)
    else:
        await message.answer(text=f'{text.class_was_adding}', reply_markup=reply.yes_or_no)
    users_data[message.from_user.id]['class_name'] = message.text
    await state.set_state(Add.confirm_class_name)


@router.message(Add.confirm_class_name, F.text)
async def confirm_class_name(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'так':
        await state.set_state(Add.day)
        await message.answer(text=f'{text.get_day}', reply_markup=reply.days)
    elif msg == 'ні' or msg == 'вихід':
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')


@router.message(Add.day, F.text)
async def weekday_selection_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    msg = message.text
    if msg.lower() == 'вихід':
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
    elif msg in schedule_tools.default_days:
        users_data[message.from_user.id]['day'] = msg
        await state.set_state(Add.schedule)
        await message.answer(text=f'{text.get_schedules}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_this_day_is_not}', reply_markup=reply.days)


@router.message(Add.schedule, F.text)
async def add_schedules_handler(message: Message, state: FSMContext) -> None:
    if message.text.lower() == 'вихід':
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
        return
    lessons = re.split(',', message.text)
    lessons = [lesson.lstrip() for lesson in lessons]
    i = 0
    while i < len(lessons):
        lessons[i] = f'{i + 1}. {lessons[i]}\n'
        i = i + 1
    name_lessons = ''
    for lesson in lessons:
        name_lessons = name_lessons + lesson
    users_data[message.from_user.id]['schedules'] = lessons
    await state.set_state(Add.confirm_schedules)
    await message.answer(text=f'<b><i>Ось що вийшло: \n{name_lessons}Все вірно?</i></b>', reply_markup=reply.yes_or_no)


@router.message(Add.confirm_schedules, F.text)
async def confirm_schedules(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    user_id = message.from_user.id
    if msg == 'так':
        school_name = users_data[user_id]['school_name']
        class_name = users_data[user_id]['class_name']
        day = users_data[user_id]['day']
        lessons = users_data[user_id]['schedules']
        schedules = deserialization(paths.schedules)
        schedule_tools.add_new_schedule(
            school_name, class_name, day, lessons, schedules)
        serialization(schedules, paths.schedules)
        del users_data[user_id]
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.schedules_added}', reply_markup=reply.main)
    elif msg == 'ні':
        await state.set_state(Add.schedule)
        await message.answer(text=f'{text.input_schedules_again}')
    elif msg == 'вихід':
        user_tools.del_user_in_state(message.from_user.id)
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')
