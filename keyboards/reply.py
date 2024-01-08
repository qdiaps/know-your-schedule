from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Розклад'),
            KeyboardButton(text='Налаштування')
        ],
        [
            KeyboardButton(text='Тех. підтримка'),
            KeyboardButton(text='Інше')
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
            KeyboardButton(text='Видалити'),
            KeyboardButton(text='Редагувати')
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

yes_or_edit_with_exit = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Так'),
            KeyboardButton(text='Змінити')
        ],
        [
            KeyboardButton(text='Вихід')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

yes_or_no_with_exit = ReplyKeyboardMarkup(
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

yes_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Так'),
            KeyboardButton(text='Ні')
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

operations = ReplyKeyboardMarkup(
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

selection_school = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Немає навч. закладу')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

selection_class = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Немає класу')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
