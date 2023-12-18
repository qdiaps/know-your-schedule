from aiogram.fsm.state import StatesGroup, State


class Add(StatesGroup):
    school_name = State()
    confirm_school_name = State()
    class_name = State()
    confirm_class_name = State()
    day = State()
    schedule = State()
    confirm_schedules = State()
