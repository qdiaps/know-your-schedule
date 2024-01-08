from aiogram.fsm.state import StatesGroup, State


class Add(StatesGroup):
    selection_operation = State()
    confirm_exit_from_editers = State()
    school_name = State()
    confirm_school_name = State()
    class_name = State()
    day = State()
    schedule = State()
    confirm_schedules = State()
    add_still_schedules = State()


class Show(StatesGroup):
    school_name = State()
    class_name = State()
    confirm = State()
    show_schedule = State()


class Delete(StatesGroup):
    selection_operation = State()
    school_name = State()
    class_name = State()
    day = State()
    confirm = State()
    

class Selection(StatesGroup):
    school_name = State()
    class_name = State()
    confirm = State()