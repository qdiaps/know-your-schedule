from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

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

schedules_operation = ReplyKeyboardMarkup(
   keyboard=[
      #[
      #   #KeyboardButton(text='Показати')
      #   #KeyboardButton(text='Редагувати')
      #]
      [
         KeyboardButton(text='Додати'),      
      #   KeyboardButton(text='Видалити')
      ]
   ],
   resize_keyboard=True,
   one_time_keyboard=True
)

main_add = ReplyKeyboardMarkup(
   keyboard=[
      [
         KeyboardButton(text='Школу'),
         KeyboardButton(text='Клас'),
         KeyboardButton(text='Розклад')
      ]
   ],
   resize_keyboard=True,
   one_time_keyboard=True
)

remove_keyboard = ReplyKeyboardRemove()

days = ReplyKeyboardMarkup(
   keyboard=[
      [
         KeyboardButton(text='Понеділок'),
         KeyboardButton(text='Вівторок')
      ],
      [
         KeyboardButton(text='Середа'),
         KeyboardButton(text='Четверг')
      ],
      [
         KeyboardButton(text='П\'ятниця'),
         KeyboardButton(text='Субота')
      ]
   ],
   resize_keyboard=True,
   one_time_keyboard=True
)