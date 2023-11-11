from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from data import text
from keyboards import reply

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
  await message.answer(text=f'{text.start_text}', reply_markup=reply.main)