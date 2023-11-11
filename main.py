"""
Copyright (c) 2023 qdiaps

Програмне забеспечення поширюється з ліцензією MIT.
Детальніше дивіться у файлі LICENSE.
"""

import asyncio

from aiogram import Bot, Dispatcher
from callbacks import user_callbacks
from handlers import commands, messages

async def main():
  answer_user = input('Потрібно запускати проксі? (y/n): ')
  token = input('Введіть токен боту: ')
  bot = Bot(token=f'{token}')
  if answer_user == 'y':
    from aiogram.client.session.aiohttp import AiohttpSession
    session = AiohttpSession(proxy='http://proxy.server:3128')
    bot = Bot(token=f'{token}', session=session)
  print('Все вірно.')
  dp = Dispatcher()
  dp.include_routers(
    commands.router,
    user_callbacks.router,
    messages.router
  )
  await bot.delete_webhook(drop_pending_updates=True)
  print('Бот працює!')
  await dp.start_polling(bot)

if __name__ == '__main__':
  asyncio.run(main())
