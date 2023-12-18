from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from data import text
from keyboards import reply
from utils import user_tools

router = Router()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    if user_tools.is_user_in_state(message.from_user.id) == False:
        await message.answer(text=f'{text.start_text}', reply_markup=reply.main)
