"""
Copyright (c) 2023 qdiaps

Програмне забеспечення поширюється з ліцензією MIT.
Детальніше дивіться у файлі LICENSE.
"""

import asyncio
import json

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

bot = None
dp = Dispatcher()

@dp.message(Command('start'))
async def command_start(message: Message):
  await message.answer(text=f'Start bot')

@dp.message()
async def echo(message: Message):
  await message.answer(text=f'Ви написали: {message.text}')

def start_settings():
  global bot
  print('Потрібно запускати проксі? (y/n)')
  answer_user = input()
  print('Введіть токен боту:')
  token = input()
  if answer_user == 'y':
    from aiogram.client.session.aiohttp import AiohttpSession
    session = AiohttpSession(proxy='http://proxy.server:3128')
    bot = Bot(token=f'{token}', session=session)
    print('Все вірно.')
  else:
    bot = Bot(token=f'{token}')
    print('Все вірно.')

async def main():
  start_settings()
  await bot.delete_webhook(drop_pending_updates=True)
  print('Бот працює!')
  await dp.start_polling(bot)

if __name__ == '__main__':
  asyncio.run(main())
