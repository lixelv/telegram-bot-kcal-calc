# from webhook import webhook_pooling
from url import *
from db import DB

sql = DB(loop, db_config)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await sql.user_exist(message.from_user.id):
        await sql.new_user(message.from_user.id, message.from_user.username)

    await message.answer('Привет!')

@dp.message_handler(sql.is_0)
async def nothing_found(message: types.Message):
    await message.answer('Ничего не найдено!')

@dp.message_handler(sql.is_1)
async def found_1(message: types.Message):
    searchment = await sql.search_1(message.from_user.id, message.text)
    result = f'`{searchment[0]}`\n' \
             f'Ккал: `{searchment[1]} ккал`\n' \
             f'Белок: `{searchment[2]} г.`\n' \
             f'Жир: `{searchment[3]} г.`\n' \
             f'Углеводы: `{searchment[4]} г.`'
    await message.answer(result, reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

@dp.message_handler(content_types='text')
async def global_search(message: types.Message):
    page = None
    if message.text == "->":
        page = 1
        await sql.page(message.from_user.id, page)
        page = sql.get_page(message.from_user.id)

    elif message.text == "<-":
        page = -1
        await sql.page(message.from_user.id, page)
        page = sql.get_page(message.from_user.id)

    else:
        await sql.set_searchment(message.from_user.id, message.text)

    result = await sql.search_p(message.from_user.id, page=page)
    kb = inline(result)
    await message.answer('Вот список ответов на ваш запрос:', reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)
    # webhook_pooling(dp, port, link, my_id)