from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data import paths, text, user_data_operation
from data.json_tools import deserialization
from keyboards import reply
from handlers.show_schedules import process_data
from handlers.add_schedules import operations
from utils.states import Selection, Add

router = Router()


async def start_selection_school_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    schedules = deserialization(paths.schedules)
    if not schedules.keys():
        await state.set_state(Add.school_name)
        await state.update_data(operation=operations[0])
        await message.answer(text=f'{text.warning_is_not_schools}')
        await message.answer(text=f'{text.get_shool_name}', reply_markup=reply.exit_state)
    else:
        builder = await process_data(state, schedules)
        await state.set_state(Selection.school_name)
        await message.answer(text='<b><i>Навчальні заклади: </i></b>', reply_markup=builder.as_markup())


@router.message(Selection.school_name, F.text)
async def message_handler(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'немає навч. закладу':
        await state.set_state(Add.school_name)
        await state.update_data(operation=operations[0])
        await message.answer(text=f'{text.get_shool_name}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')


@router.callback_query(Selection.school_name, F.data)
async def selection_class_handler(callback: CallbackQuery, state: FSMContext) -> None:
    schedules = deserialization(paths.schedules)
    await state.update_data(school_name=callback.data)
    if not schedules[callback.data].keys():
        await state.set_state(Add.class_name)
        await state.update_data(operation=operations[1])
        await callback.message.answer(text=f'{text.get_class_name}', reply_markup=reply.exit_state)
    else:
        builder = await process_data(state, schedules[callback.data])
        await state.set_state(Selection.class_name)
        await callback.message.delete()
        await callback.message.answer(text=f'{text.info_if_is_not_classes}', reply_markup=reply.selection_class)
        await callback.message.answer(text='<b><i>Класи: </i></b>', reply_markup=builder.as_markup())
    await callback.answer()


@router.message(Selection.class_name, F.text)
async def message_handler_class(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    if msg == 'немає класу':
        await state.set_state(Add.class_name)
        await state.update_data(operation=operations[1])
        await message.answer(text=f'{text.get_class_name}', reply_markup=reply.exit_state)
    else:
        await message.answer(text=f'{text.warning_is_not_command}')

    
@router.callback_query(Selection.class_name, F.data)
async def confirm_handler(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    output_text = f'<b><i>Навчальний заклад: </i></b>{data["school_name"]}<b><i>, клас: </i></b>{callback.data}.'
    await state.update_data(class_name=callback.data)
    await state.set_state(Selection.confirm)
    await callback.message.delete()
    await callback.message.answer(text=f'<b><i>Все вірно? </i></b>{output_text}', reply_markup=reply.yes_or_no)
    await callback.answer()


@router.message(Selection.confirm, F.text)
async def confirm_message_handler(message: Message, state: FSMContext) -> None:
    msg = message.text.lower()
    schedules = deserialization(paths.schedules)
    if msg == 'так':
        data = await state.get_data()
        await user_data_operation.connect_school_with_user(data['school_name'], message.from_user)
        await user_data_operation.connect_class_with_user(data['class_name'], message.from_user)
        await state.clear()
        await message.answer(text=f'{text.selection_school_and_class_good}', reply_markup=reply.main)
    elif msg == 'ні':
        builder = await process_data(state, schedules)
        await state.set_state(Selection.school_name)
        await message.answer(text=f'{text.get_again_school_name}', reply_markup=reply.selection_school)
        await message.answer(text='<b><i>Навчальні заклади:</i></b>', reply_markup=builder.as_markup())
    else:
        await message.answer(text=f'{text.warning_is_not_command}')