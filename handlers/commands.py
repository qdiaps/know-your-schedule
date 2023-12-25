from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from data import text
from keyboards import reply

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=f'{text.start_text}', reply_markup=reply.main)


@router.message(F.text.lower() == 'вихід')
async def exit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f'{text.next_button}', reply_markup=reply.main)
