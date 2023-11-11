from aiogram import Router
from aiogram.types import Message
from data import text
from keyboards import inline

router = Router()

@router.message()
async def message_handler(message: Message):
  msg = message.text.lower()
  if msg == 'розклад':
    await message.answer(text=f'{text.command_schedule}', reply_markup=inline.schedules_operation)
  else:
    await message.answer(text=f'{text.warning_is_not_command}')