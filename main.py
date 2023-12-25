"""
Copyright (c) 2023 qdiaps

Програмне забеспечення поширюється з ліцензією MIT.
Детальніше дивіться у файлі LICENSE.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import commands, messages, add_schedules, show_schedules, delete_schedules
from callbacks import inline_navigation
from middlewares.check_chat_type import CheckChatType
from data import paths


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
    print('Все вірно.')
    dp = Dispatcher()
    dp.message.middleware(CheckChatType())
    dp.include_routers(
        commands.router,
        inline_navigation.router,
        add_schedules.router,
        show_schedules.router,
        delete_schedules.router,
        messages.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    print('Бот працює!')
    logging.basicConfig(level=logging.INFO, filename=f'log/{paths.log}', 
        format='%(asctime)s %(levelname)s | %(message)s | %(filename)s %(funcName)s')
    logging.info('---- Запуск бота ----')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
