import mysql

from url import *
from webhook import webhook_pooling

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not sql.user_exist(message.from_user.id):
        sql.new_user(message.from_user.id, message.from_user.username)
    await bot.send_message(message.from_user.id, 'Привет!')

if __name__ == '__main__':
    webhook_pooling(dp, port, link, my_id)