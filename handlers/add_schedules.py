import re
import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils.states import Add
from keyboards import reply
from data import paths, schedule_tools, text, user_data_operation
from data.user_data_operation import Rangs
from data.json_tools import deserialization, serialization

router = Router()
users_data = {}
operations = ('Школу', 'Клас', 'Розклад')
min_count_editers = 1

@router.message(StateFilter(None), F.text.lower().in_(['додати']))
async def start_adding_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Add.selection_operation)
    await message.answer(text=f'{text.what_to_add}', reply_markup=reply.operations)


@router.message(Add.selection_operation, F.text)
async def selection_operation_handler(message: Message, state: FSMContext) -> None:
    if message.text in operations:
        await state.update_data(operation=message.text)
        user_id = message.from_user.id
        connecting_info = await user_data_operation.get_connecting_info(user_id)
        editers = await user_data_operation.get_editers_with_connecting_info(connecting_info)
        if message.text in [operations[0], operations[1]] and str(user_id) in editers:
            await state.set_state(Add.confirm_exit_from_editers)
            if len(editers) == min_count_editers:
                await message.answer(text=f'{text.confirm_exit_from_editers1}', reply_markup=reply.exit_state)
            elif len(editers) > min_count_editers:
                await message.answer(text=f'{text.confirm_exit_from_editers2}', reply_markup=reply.exit_state)
        else:
            await state.set_state(Add.school_name)
            await message.answer(text=f'{text.get_shool_name}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_is_not_command}', reply_markup=reply.operations)


@router.message(Add.confirm_exit_from_editers, F.text)
async def confirm_exit_from_editers_handler(message: Message, state: FSMContext) -> None:
    if message.text.lower() == 'я погоджуюсь вийти':
        await user_data_operation.change_rang(user_data_operation.Rangs.New, message.from_user.id)
        logging.info(f'{message.from_user.id} тепер не редактор -> {await user_data_operation.get_connecting_info(message.from_user.id)}')
        await message.answer(text=f'{text.is_exit_from_editers}')
        data = await state.get_data()
        connecting_info = await user_data_operation.get_connecting_info(message.from_user.id)
        if data['operation'] == operations[1]:
            if connecting_info[0] != None:
                await state.set_state(Add.confirm_school_name)
                await state.update_data(school_name=connecting_info[0])
                await message.answer(text=f'<b><i>Все вірно? Навчальний заклад: </i></b>{connecting_info[0]}', reply_markup=reply.yes_or_no_with_exit)
                return
        await state.set_state(Add.school_name)
        await message.answer(text=f'{text.get_shool_name}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_is_not_command}', reply_markup=reply.exit_state)


@router.message(Add.confirm_school_name, F.text)
async def confirm_school_name(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'так':
        await state.set_state(Add.class_name)
        await message.answer(text=f'{text.get_class_name}', reply_markup=reply.exit_state)
    elif msg == 'ні':
        await state.set_state(Add.school_name)
        await message.answer(text=f'{text.get_shool_name}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')
    

@router.message(Add.school_name, F.text)
async def add_school_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    schedules = deserialization(paths.schedules)
    if message.text not in schedules.keys():
        data = await state.get_data()
        if data['operation'] != operations[0]:
            await message.answer(text=f'{text.warning_is_not_school}', reply_markup=reply.exit_state)
        else:
            if '\n' in message.text:
                await message.answer(text=f'{text.warning_check_to_line_break}')
                return
            schedule_tools.add_new_school(message.text, schedules)
            serialization(schedules, paths.schedules)
            logging.info(f'{user_id} Додав нову школу в JSON -> {message.text}')
            await user_data_operation.connect_school_with_user(message.text, message.from_user)
            await user_data_operation.reset_connection_class(user_id)
            await message.answer(text=f'{text.school_added}')
            await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
            await state.clear()
    else:
        data = await state.get_data()
        if data['operation'] != operations[0]:
            await state.update_data(school_name=message.text)
            await state.set_state(Add.class_name)
            await message.answer(text=f'{text.get_class_name}', reply_markup=reply.exit_state)
        else:
            await message.answer(text=f'{text.school_was_adding}', reply_markup=reply.exit_state)


@router.message(Add.class_name, F.text)
async def add_class_handler(message: Message, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    data = await state.get_data()
    if message.text not in schedules[data['school_name']].keys():
        if data['operation'] == operations[2]:
            await message.answer(text=f'{text.warning_is_not_class}', reply_markup=reply.exit_state)
        else:
            if '\n' in message.text:
                await message.answer(text=f'{text.warning_check_to_line_break}')
                return
            schedule_tools.add_new_class(data['school_name'], message.text, schedules)
            serialization(schedules, paths.schedules)
            logging.info(f'{message.from_user.id} Додав новий клас в JSON -> {data["school_name"]} - {message.text}')
            await user_data_operation.change_rang(Rangs.Editer, message.from_user.id)
            await user_data_operation.connect_school_with_user(data['school_name'], message.from_user)
            await user_data_operation.connect_class_with_user(message.text, message.from_user)
            await message.answer(text=f'{text.class_added}')
            await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
            await state.clear()
    else:
        data = await state.get_data()
        if data['operation'] == operations[2]:
            await state.update_data(class_name=message.text)
            await state.set_state(Add.day)
            await message.answer(text=f'{text.get_day}', reply_markup=reply.days)
        else:
            await message.answer(text=f'{text.class_was_adding}', reply_markup=reply.exit_state)


@router.message(Add.day, F.text)
async def weekday_selection_handler(message: Message, state: FSMContext) -> None:
    msg = message.text
    if msg in schedule_tools.default_days:
        schedules = deserialization(paths.schedules)
        data = await state.get_data()
        if len(schedules[data['school_name']][data['class_name']][msg]) > 0:
            await message.answer(text=f'{text.warning_schedules_added}', reply_markup=reply.days)
        else:
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
    await message.answer(text=f'<b><i>Ось що вийшло: \n{name_lessons}Все вірно?</i></b>', reply_markup=reply.yes_or_no_with_exit)


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
        logging.info(f'{message.from_user.id} додав новий розклад в JSON -> {school_name} - {class_name} - {lessons}')
        await state.set_state(Add.add_still_schedules)
        await message.answer(text=f'{text.schedules_added}', reply_markup=reply.yes_or_no_with_exit)
    elif msg == 'ні':
        await state.set_state(Add.schedule)
        await message.answer(text=f'{text.input_schedules_again}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_is_not_command}', reply_markup=reply.yes_or_no_with_exit)


@router.message(Add.add_still_schedules, F.text)
async def confirm_add_still_shedules(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'так':
        await state.set_state(Add.day)
        await message.answer(text=f'{text.get_day}', reply_markup=reply.days)
    elif msg == 'ні':
        await state.clear()
        await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
    else:
        await message.answer(text=f'{text.warning_is_not_command}', reply_markup=reply.yes_or_no_with_exit)