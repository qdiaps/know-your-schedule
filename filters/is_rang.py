from data import user_data_operation
from data.user_data_operation import Rangs, rangs


async def checkLevelRang(min_rang_level: Rangs, user_id: int | str) -> bool:
    user_rang = await user_data_operation.get_rang(user_id)
    return rangs.index(user_rang) >= min_rang_level.value