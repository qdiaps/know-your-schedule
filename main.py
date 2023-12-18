"""
Copyright (c) 2023 qdiaps

Програмне забеспечення поширюється з ліцензією MIT.
Детальніше дивіться у файлі LICENSE.
"""

import asyncio

from aiogram import Bot, Dispatcher
from handlers import commands, messages, add_schedules
from data import paths, json_tools

def settings() -> None:
    user_in_state = json_tools.deserialization(paths.user_in_state)
    user_in_state = {}
    json_tools.serialization(user_in_state, paths.user_in_state)


def start_bot(token: str, is_proxy: bool):
    bot = Bot(token=f'{token}', parse_mode='HTML')
    if is_proxy == True:
        from aiogram.client.session.aiohttp import AiohttpSession
        session = AiohttpSession(proxy='http://proxy.server:3128')
        bot = Bot(token=f'{token}', session=session)
    return bot


def get_user_input(message: str = '') -> str:
    return input(f'{message}')


async def main() -> None:
    user_input_is_proxy = get_user_input('Потрібно запускати проксі? (y/n): ')
    is_proxy = True if user_input_is_proxy == 'y' else False
    token = get_user_input('Введіть токен боту: ')
    bot = start_bot(token, is_proxy)
    settings()
    print('Все вірно.')
    dp = Dispatcher()
    dp.include_routers(
        commands.router,
        add_schedules.router,
        messages.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    print('Бот працює!')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
