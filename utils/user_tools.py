from data.json_tools import deserialization, serialization
from data import paths


def is_user_in_state(id: int | str) -> bool:
    user_in_state = deserialization(paths.user_in_state)
    return str(id) in user_in_state.keys()


def set_user_in_state(id: int | str) -> None:
    if is_user_in_state(id) == False:
        user_in_state = deserialization(paths.user_in_state)
        user_in_state[id] = '0'
        serialization(user_in_state, paths.user_in_state)


def del_user_in_state(id: int | str) -> None:
    if is_user_in_state(id) == True:
        user_in_state = deserialization(paths.user_in_state)
        del user_in_state[str(id)]
        serialization(user_in_state, paths.user_in_state)
