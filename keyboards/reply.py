from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
   keyboard=[
      [
         KeyboardButton(text='Розклад')
      ]
   ],
   resize_keyboard=True,
   one_time_keyboard=True,
   input_field_placeholder='Оберіть операцію...'
)