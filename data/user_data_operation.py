import logging

from enum import Enum
from aiogram.types import User
from data import paths
from data.json_tools import deserialization, serialization

rangs = ('Новий', 'Редактор', 'Адмін')


class Rangs(Enum):
    New = 0
    Editer = 1
    Admin = 2


class Data(Enum):
    Rang = 0
    Connect_info = 1
    Contact = 2


async def get_connecting_info(user_id: int | str) -> tuple:
    # connecting_info[0] = users[str(user_id)][Data.Connect_info.value][0]
    # connecting_info[1] = users[str(user_id)][Data.Connect_info.value][1]
    users = deserialization(paths.users)
    school_name = users[str(user_id)][Data.Connect_info.value][0]
    class_name = users[str(user_id)][Data.Connect_info.value][1]
    schedules = deserialization(paths.schedules)
    result = [None, None]
    if school_name in schedules.keys():
        result[0] = school_name
        if class_name in schedules[school_name].keys():
            result[1] = class_name
    users[str(user_id)][Data.Connect_info.value] = result
    serialization(users, paths.users)
    return result


async def get_user_contact(user_data: dict) -> tuple:
    username = user_data.username if user_data.username != None else None
    full_name = user_data.full_name if user_data.full_name != None else None
    return [username, full_name]


async def check_user_in_json(user_id: int | str, json_file: dict) -> bool:
    return str(user_id) in json_file.keys()


async def update_user_info(user_data: User, json_file: dict) -> None:
    if await check_user_in_json(user_data, json_file):
        json_file[user_data.id][Data.Contact.value] = await get_user_contact(user_data)
        serialization(json_file, paths.users)


async def add_new_user_to_json(user_data: User) -> None:
    if user_data == None:
        return
    users = deserialization(paths.users)
    if await check_user_in_json(user_data.id, users):
        await update_user_info(user_data, users)
    else:
        users[user_data.id] = [
            rangs[Rangs.New.value],
            [None, None],
            await get_user_contact(user_data),
        ]
        serialization(users, paths.users)


async def connect_school_with_user(school_name: str, user_data: User) -> None:
    users = deserialization(paths.users)
    if await check_user_in_json(user_data.id, users) == False:
        await add_new_user_to_json(user_data)
    users[str(user_data.id)][Data.Connect_info.value][0] = school_name
    serialization(users, paths.users)


async def connect_class_with_user(class_name: str, user_data: User) -> None:
    users = deserialization(paths.users)
    if await check_user_in_json(user_data.id, users) == False:
        await add_new_user_to_json(user_data)
    users[str(user_data.id)][Data.Connect_info.value][1] = class_name
    serialization(users, paths.users)


async def change_rang(new_rang: Rangs, user_id: str | int) -> None:
    users = deserialization(paths.users)
    if await check_user_in_json(user_id, users):
        if new_rang != None:
            users[str(user_id)][Data.Rang.value] = rangs[new_rang.value]
            serialization(users, paths.users)


async def get_rang(user_id: int | str) -> str:
    users = deserialization(paths.users)
    return users[str(user_id)][Data.Rang.value]


async def reset_connection_info(user_id: int | str) -> None:
    users = deserialization(paths.users)
    users[str(user_id)][Data.Connect_info.value][0] = None
    users[str(user_id)][Data.Connect_info.value][1] = None
    serialization(users, paths.users)


async def reset_connection_class(user_id: int | str) -> None:
    users = deserialization(paths.users)
    users[str(user_id)][Data.Connect_info.value][1] = None
    serialization(users, paths.users)


async def get_all_users_with_rang(rang: Rangs) -> dict:
    users = deserialization(paths.users)
    result = {}
    for user_id in users.keys():
        if users[user_id][Data.Rang.value] == rangs[rang.value]:
            result[user_id] = users[user_id]
    return result


async def get_editers_with_connecting_info(connecting_info: tuple) -> tuple:
    editers = await get_all_users_with_rang(Rangs.Editer)
    result = []
    for editer in editers:
        if editers[editer][Data.Connect_info.value] == connecting_info:
            result.append(editer)
    return result