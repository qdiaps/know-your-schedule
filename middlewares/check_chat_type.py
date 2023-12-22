from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery


class CheckChatType(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        msg = None
        if type(event) == Message:
            msg = event
        elif type(event) == CallbackQuery:
            msg = event.message

        if msg != None and msg.chat.type == 'private':
            return await handler(event, data)