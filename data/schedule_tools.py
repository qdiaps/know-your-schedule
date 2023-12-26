default_days = [
    'Понеділок', 'Вівторок', 'Середа', 'Четверг', 'П\'ятниця', 'Субота'
]


def delete_schedule(school_name: str, class_name: str, day: str, obj: dict) -> None:
    if school_name in obj.keys():
        if class_name in obj[school_name].keys():
            obj[school_name][class_name][day] = []


def delete_class(school_name: str, class_name: str, obj: dict) -> None:
    if school_name in obj.keys():
        if class_name in obj[school_name].keys():
            del obj[school_name][class_name]


def delete_school(school_name: str, obj: dict) -> None:
    if school_name in obj.keys():
        del obj[school_name]


def edit_schedule(school_name: str, class_name: str, day: str, schedules: list, obj: object) -> None:
    if school_name in obj.keys():
        if class_name in obj[school_name].keys():
            obj[school_name][class_name][day] = schedules


def edit_class(school_name: str, class_name: str, class_name_edited, obj: object) -> None:
    if school_name in obj.keys():
        if class_name in obj[school_name].keys():
            if class_name_edited not in obj[school_name].keys():
                obj[school_name][class_name_edited] = obj[school_name][class_name]
                del obj[school_name][class_name]


def edit_school(school_name: str, school_name_edited: str, obj: object) -> None:
    if school_name in obj.keys():
        if school_name_edited not in obj.keys():
            obj[school_name_edited] = obj[school_name]
            del obj[school_name]


def add_new_schedule(school_name: str, class_name: str, day: str, schedules: list, obj: dict) -> None:
    if school_name in obj.keys():
        if class_name in obj[school_name].keys():
            obj[school_name][class_name][day] = schedules


def add_new_class(school_name: str, class_name: str, obj: dict) -> None:
    if school_name in obj.keys():
        if class_name not in obj[school_name].keys():
            obj[school_name][class_name] = {}
            for day in default_days:
                obj[school_name][class_name][day] = []


def add_new_school(school_name: str, obj: dict) -> None:
    if school_name not in obj.keys():
        obj[school_name] = {}
