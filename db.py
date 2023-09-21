import aiomysql
import asyncio
from aiogram import types
from url import page_size, my_id


class DB:
    def __init__(self, db_config, loop):
        self.loop = loop
        self.pool = loop.run_until_complete(self.init_pool(host=db_config['host'], user=db_config['user'], password=db_config['password'], db=db_config['database'], port=3306))
        loop.create_task(self.keep_alive())

    async def init_pool(self, host, port, user, password, db):
        pool = await aiomysql.create_pool(
            host=host, port=port,
            user=user, password=password,
            db=db, loop=self.loop
        )
        return pool

    async def keep_alive(self):
        while True:
            result = await self.read('SELECT 1;')
            await asyncio.sleep(14400)

    async def do(self, sql, values=()):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, values)
                await conn.commit()

    async def read(self, sql, values=(), one=False):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, values)
                if one:
                    return await cur.fetchone()
                else:
                    return await cur.fetchall()

    async def is_0(self, message: types.Message):
        result = await self.search(message.from_user.id, message.text)
        result = not bool(result)
        return result

    async def is_1(self, message: types.Message):
        result = await self.read('SELECT id FROM product WHERE LOWER(name) = LOWER(%s)', (message.text,))
        result = bool(len(result) == 1)
        return result

    async def set_searchment(self, user_id, searchment):
        await self.do('UPDATE user SET searchment = %s WHERE id = %s', (searchment, user_id))

    async def search_1(self, user_id, resp) -> tuple:
        return await self.read("SELECT name, kcal, protein, fat, carbonates FROM product WHERE LOWER(name) LIKE %s", ('%'+resp.lower()+'%',), one=True)

    async def search_p(self, user_id, page=None) -> tuple:
        if page is None:
            page = await self.read("SELECT page FROM user WHERE id = %s", (user_id,), one=True)
            page = page[0]

        resp = await self.read("SELECT LOWER(searchment) FROM user WHERE id = %s;", (user_id,), one=True)
        resp = resp[0]

        result = await self.read("SELECT name FROM product WHERE LOWER(name) LIKE %s AND user_id IN (%s, %s) LIMIT %s OFFSET %s;", (f"%{resp.lower()}%", my_id, user_id, page_size, page_size*page))
        return result

    async def search(self, user_id, resp) -> tuple:
        return await self.read("SELECT name FROM product WHERE LOWER(name) LIKE %s AND user_id IN (%s, %s)", (f"%{resp.lower()}%", my_id, user_id))

    async def user_exist(self, user_id) -> bool:
        return bool(await self.read('SELECT id FROM user WHERE id = %s', (user_id,)))

    async def new_user(self, user_id, username) -> None:
        await self.do('INSERT INTO user(id, name) VALUES (%s, %s)', (user_id, username))


