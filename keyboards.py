from aiogram.types import (
   ReplyKeyboardMarkup,
   KeyboardButton,
   InlineKeyboardMarkup,
   InlineKeyboardButton
)

start_button = ReplyKeyboardMarkup(
   keyboard=[
      [
         KeyboardButton(text='Розклад')
      ]
   ],
   resize_keyboard=True,
   one_time_keyboard=True,
   input_field_placeholder='Оберіть операцію...'
)

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