import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message
from data import text
from keyboards import reply

router = Router()

@router.message(F.text)
async def message_handler(message: Message) -> None:
  msg = message.text.lower()
  if msg == 'розклад':
    await message.answer(text=f'{text.command_schedule}', reply_markup=reply.schedules_operation)
  else:
    await message.answer(text=f'{text.warning_is_not_command}')