from asyncio import get_event_loop
from aiogram import Bot, Dispatcher, types
from envparse import env

env.read_envfile('.env')
db_config = {
    "host": env('HOST_'),
    "user": env('USER_'),
    "password": env('PASSWORD_'),
    "database": env('DB_'),
    "port": 3306
}

token = env('TELEGRAM')
my_id = int(env('MYID'))

bot = Bot(token)
dp = Dispatcher(bot)

loop = get_event_loop()

page_size = 40

next_ = "Далее ▶️"
previous_ = "◀️ Назад"

def inline(lst: list, count, page):

    kb: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup()

    if page != 0:
        kb.add(types.KeyboardButton(previous_))

    for key in lst:
        kb.add(types.KeyboardButton(key[0]))

    if page < count // page_size:
        kb.add(types.KeyboardButton(next_))

    return kb
