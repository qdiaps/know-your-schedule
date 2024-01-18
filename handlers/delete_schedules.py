import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards import reply, builders
from data import text, paths, user_data_operation
from data.json_tools import deserialization, serialization
from data.user_data_operation import Rangs
from utils.states import Delete
from handlers.show_schedules import process_data
from filters import is_rang

router = Router()
operations = ('Школу', 'Клас', 'Розклад')


@router.message(StateFilter(None), F.text.lower() == 'видалити')
async def selection_operation_handler(message: Message, state: FSMContext) -> None:
    if await is_rang.checkLevelRang(Rangs.Editer, message.from_user.id) == False:
        await message.answer(text=f'{text.warning_is_low_rang}', reply_markup=reply.main)
    else:
        await state.clear()
        schedules = deserialization(paths.schedules)
        if not schedules.keys():
            await message.answer(text=f'{text.warning_is_not_schools}', reply_markup=reply.main)
            return
        await state.set_state(Delete.selection_operation)
        await message.answer(text=f'{text.what_to_remove}', reply_markup=reply.operations)


@router.message(Delete.selection_operation, F.text)
async def selection_school_handler(message: Message, state: FSMContext) -> None:
    if message.text in operations:
        if message.text == operations[0]:
            if await is_rang.checkLevelRang(Rangs.Admin, message.from_user.id) == False:
                await message.answer(text=f'{text.warning_is_low_rang}', reply_markup=reply.operations)
                return
        schedules = deserialization(paths.schedules)
        builder = await process_data(state, schedules)
        await state.update_data(operation=message.text)
        await state.set_state(Delete.school_name)
        await message.answer(text=f'{text.get_shool_name_for_delete}', reply_markup=reply.exit_state)
        await message.answer(text='<b><i>Школи: </i></b>', reply_markup=builder.as_markup())
    else:
        await message.answer(text=f'{text.warning_is_not_command}', reply_markup=reply.operations)


@router.callback_query(Delete.school_name, F.data)
async def selection_class_handler(callback: CallbackQuery, state: FSMContext) -> None:
    connection_info = await user_data_operation.get_connecting_info(callback.from_user.id)
    if callback.data == connection_info[0]:
        data = await state.get_data()
        await callback.message.delete()
        await state.update_data(school_name=callback.data)
        if data['operation'] == operations[0]:
            await confirm_delete(callback.message, state)
        else:
            schedules = deserialization(paths.schedules)
            if not schedules[callback.data].keys():
                await callback.message.answer(text=f'{text.warning_is_not_classes}')
            else:
                builder = await process_data(state, schedules[callback.data])
                await state.set_state(Delete.class_name)
                await callback.message.answer(text='<b><i>Класи: </i></b>', reply_markup=builder.as_markup())
    else:
        await callback.message.answer(text=f'{text.warning_get_school_created}')
    await callback.answer()


@router.message(Delete.school_name, F.text)
async def message_handler_class(message: Message) -> None:
    await message.answer(text=f'{text.warning_is_not_command}')


@router.callback_query(Delete.class_name, F.data)
async def selection_weekday_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.update_data(class_name=callback.data)
    connection_info = await user_data_operation.get_connecting_info(callback.from_user.id)
    if [data['school_name'], callback.data] == connection_info:
        await callback.message.delete()
        if data['operation'] == operations[1]:
            await confirm_delete(callback.message, state)
        else:
            schedules = deserialization(paths.schedules)
            schedules = schedules[data['school_name']][callback.data]
            weekdays = []
            for schedule in schedules:
                if not schedules[schedule]:
                    continue
                weekdays.append(schedule)
            if not weekdays:
                await state.clear()
                await callback.message.answer(text=f'{text.warning_is_not_schedules_in_classes}', reply_markup=reply.main)
            else:
                builder = builders.create_page(weekdays)
                await state.set_state(Delete.day)
                await callback.message.answer(text=f'{text.get_day_for_delete}', reply_markup=builder.as_markup())
    else:
        await callback.message.answer(text=f'{text.warning_get_class_created}')
    await callback.answer()


@router.message(Delete.class_name, F.text)
async def message_handler_weekday(message: Message) -> None:
    await message.answer(text=f'{text.warning_is_not_command}')


@router.callback_query(Delete.day, F.data)
async def confirm_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(day=callback.data)
    await callback.message.delete()
    await confirm_delete(callback.message, state)
    await callback.answer()


@router.message(Delete.day, F.text)
async def message_handler_confirm(message: Message) -> None:
    await message.answer(text=f'{text.warning_is_not_command}')


async def confirm_delete(message: Message, state: FSMContext) -> None:
    await state.set_state(Delete.confirm)
    await message.answer(text=f'{text.confirm_deleting}')


async def delete(data: dict, user_id: str | int) -> None:
    schedules = deserialization(paths.schedules)
    if data['operation'] == operations[0]:
        logging.info(f'Видалив школу з JSON -> {data["school_name"]}')
        del schedules[data['school_name']]
        await user_data_operation.reset_connection_info(user_id)
    elif data['operation'] == operations[1]:
        logging.info(f'Видалив клас з JSON -> {data["class_name"]}')
        del schedules[data['school_name']][data['class_name']]
        await user_data_operation.reset_connection_class(user_id)
    elif data['operation'] == operations[2]:
        logging.info(f'Видалив розклад з JSON -> {schedules[data["school_name"]][data["class_name"]][data["day"]]}')
        schedules[data['school_name']][data['class_name']][data['day']] = []
    serialization(schedules, paths.schedules)


@router.message(Delete.confirm, F.text)
async def delete_from_schedules(message: Message, state: FSMContext) -> None:
    if message.text == 'Я погоджуюсь видалити':
        user_id = message.from_user.id
        data = await state.get_data()
        if data['operation'] != operations[2]:
            await user_data_operation.change_rang(Rangs.New, user_id)
            await user_data_operation.reset_connection_info(user_id)
        await delete(data, user_id)
        await state.clear()
        await message.answer(text=f'{text.is_deleted}', reply_markup=reply.main)
    else:
        await message.answer(text=f'{text.warning_to_check_message}')
