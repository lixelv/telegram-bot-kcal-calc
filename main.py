# from webhook import webhook_pooling
from url import *
from aiogram import types, executor
from db import DB

sql = DB(loop, db_config)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await sql.user_exist(message.from_user.id):
        await sql.new_user(message.from_user.id, message.from_user.username)

    await message.answer('Привет!')

@dp.message_handler(lambda message: len(message.text) <= 3)
async def bigger_then_3(message: types.Message):
    await message.answer('Запрос должен быть длиннее 3 символов!')

@dp.message_handler(sql.is_1)
async def found_1(message: types.Message):
    searchment = await sql.search_1(message.from_user.id, message.text)
    result = f'`{searchment[0]}`\n' \
             f'Ккал: `{searchment[1]} ккал`\n' \
             f'Белок: `{searchment[2]} г.`\n' \
             f'Жир: `{searchment[3]} г.`\n' \
             f'Углеводы: `{searchment[4]} г.`' \
             f'Волокна: `{searchment[5]} г.`\n'

    print(searchment[6])

    await message.answer(result, reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

@dp.message_handler(content_types='text')
async def global_search(message: types.Message):
    if message.text == next_:
        page = 1
        await sql.page(message.from_user.id, page)
        page = await sql.get_page(message.from_user.id)

    elif message.text == previous_:
        page = -1
        await sql.page(message.from_user.id, page)
        page = await sql.get_page(message.from_user.id)

    else:
        page = 0
        await sql.set_searchment(message.from_user.id, message.text)
        await sql.page(message.from_user.id, page)

    result = await sql.search_p(message.from_user.id, page=page)
    if result:
        count = await sql.count(message.from_user.id)
        print(count)
        kb = inline(result, count, page)
        await message.answer('Вот список ответов на ваш запрос:', reply_markup=kb)

    else:
        await message.answer('Ничего не найдено!')

if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)
    # webhook_pooling(dp, port, link, my_id)