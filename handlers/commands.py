from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from data import text, paths, user_data_operation
from data.json_tools import deserialization
from keyboards import reply
from handlers.selection_school import start_selection_school_handler

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    users = deserialization(paths.users)
    user_in_json = await user_data_operation.check_user_in_json(message.from_user.id, users)
    await user_data_operation.add_new_user_to_json(message.from_user)
    if user_in_json == False:
        await message.answer(text=f'{text.start_text2}', reply_markup=reply.selection_school)
        await start_selection_school_handler(message, state)
    else:
        await message.answer(text=f'{text.start_text1}', reply_markup=reply.main)


@router.message(F.text.lower() == 'вихід')
async def exit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
