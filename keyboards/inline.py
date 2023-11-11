from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

schedules_operation = InlineKeyboardMarkup(
   inline_keyboard=[
      [
         InlineKeyboardButton(text='Показати', callback_data='show'),
         InlineKeyboardButton(text='Редагувати', callback_data='edit')
      ],
      [
         InlineKeyboardButton(text='Додати', callback_data='add'),      
         InlineKeyboardButton(text='Видалити', callback_data='delete')
      ]
   ]
)