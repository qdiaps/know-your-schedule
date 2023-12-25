def split_into_groups(values: list, size_groups: int, start_key: int = 0) -> dict:
    i = start_key
    temp = []
    dict_return = {}
    for value in values:
        temp.append(value)
        if len(temp) == size_groups:
            dict_return[i] = temp
            i += 1
            temp = []
    if temp:
        dict_return[i] = temp
    return dict_return
