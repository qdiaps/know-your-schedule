from aiogram import Router
from aiogram.types import CallbackQuery
from data import text, json_tools, paths

router = Router()

@router.callback_query()
async def inline_command_handler(call: CallbackQuery):
   schedules = json_tools.deserialization(paths.schedules)

   if call.data == 'show':
      if schedules == None:
         await call.message.answer(text=f'{text.warning_schedule_is_none}')
      else:
         await call.message.answer(text=f'{text.inline_show}')
   elif call.data == 'add':
      await call.message.answer(text=f'{text.inline_add}')
   elif call.data == 'edit':
      await call.message.answer(text=f'{text.inline_edit}')
   elif call.data == 'delete':
      await call.message.answer(text=f'{text.inline_delete}')