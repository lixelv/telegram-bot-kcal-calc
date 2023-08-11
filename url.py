from aiogram import Bot, Dispatcher, types
from envparse import env
from db import DB

sql = DB('data.db')

env.read_envfile('.env')
token = env('TELEGRAM')
port = env('PORT')
link = env('LINK')
my_id = env('MY_ID')
bot = Bot(token)
dp = Dispatcher(bot)