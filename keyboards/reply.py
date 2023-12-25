from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Розклад')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

schedules_operation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Додати'),
            KeyboardButton(text='Показати')
        ],
        [
            KeyboardButton(text='Вихід')
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
        ],
        [
            KeyboardButton(text='Вихід')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Так'),
            KeyboardButton(text='Ні')
        ],
        [
            KeyboardButton(text='Вихід')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

exit_state = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Вихід')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
