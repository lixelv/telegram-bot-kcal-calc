# from webhook import webhook_pooling
from url import *
from db import DB

sql = DB(db_config, loop)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not sql.user_exist(message.from_user.id):
        sql.new_user(message.from_user.id, message.from_user.username)

    await message.answer('Привет!')

@dp.message_handler(content_types='text')
async def global_search(message: types.Message):
    text = message.text
    sql.set_searchment(message.from_user.id, message.text)
    result = sql.search_p(message.from_user.id, page=0)
    if not result:
        await nothing_found(message)
    elif (message.text,) in result:
        await found_1(message)
    else:
        kb = inline(result)
        await message.answer('Вот список ответов на ваш запрос:', reply_markup=kb)


async def nothing_found(message: types.Message):
    await message.answer('Ничего не найдено!')


async def found_1(message: types.Message):
    searchment = sql.search_1(message.from_user.id, message.text)
    result = f'`{searchment[0]}`\n' \
             f'Ккал: `{searchment[1]} ккал`\n' \
             f'Белок: `{searchment[2]} г.`\n' \
             f'Жир: `{searchment[3]} г.`\n' \
             f'Углеводы: `{searchment[4]} г.`'
    await message.answer(result, reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)
    # webhook_pooling(dp, port, link, my_id)