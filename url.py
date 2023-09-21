from aiogram.dispatcher.filters import Command
from asyncio import get_event_loop
from aiogram import Bot, Dispatcher, types, executor
from envparse import env
import asyncio

env.read_envfile('.env')
db_config = {
    "host": env('HOST_'),
    "user": env('USER_'),
    "password": env('PASSWORD_'),
    "database": env('DB_')
}

token = env('TELEGRAM')
my_id = env('MYID')

bot = Bot(token)
dp = Dispatcher(bot)

loop = get_event_loop()

page_size = 40

def inline(lst: list):
    kb: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup()
    for key in lst:
        kb.add(types.KeyboardButton(key[0]))
    return kb
