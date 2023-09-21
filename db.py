import asyncio
from aiogram import types
from url import page_size, my_id
import pymysql


class DB:
    def __init__(self, db_config, loop):
        self.connect = pymysql.connect(**db_config)
        self.cursor = self.connect.cursor()
        self.loop = loop
        loop.create_task(self.keep_alive())

    async def keep_alive(self):
        while True:
            result = self.read('SELECT 1;')
            await asyncio.sleep(14400)

    def do(self, sql, values=()):
        self.cursor.execute(sql, values)
        self.connect.commit()

    def read(self, sql, values=(), one=False):
        self.cursor.execute(sql, values)
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def is_0(self, message: types.Message):
        result = self.search(message.from_user.id, message.text)
        result = not bool(result)
        return result

    def is_1(self, message: types.Message):
        result = self.read('SELECT id FROM product WHERE name = %s', (message.text,))
        result = bool(len(result) == 1)
        return result

    def set_searchment(self, user_id, searchment):
        self.do('UPDATE user SET searchment = %s WHERE id = %s', (searchment, user_id))

    def search_1(self, user_id, resp) -> tuple:
        return self.read("SELECT name, kcal, protein, fat, carbonates FROM product WHERE name = %s AND user_id IN (%s, %s)", (resp, my_id, user_id), one=True)

    def search_p(self, user_id, page=None) -> tuple:
        if page is None:
            page = self.read("SELECT page FROM user WHERE id = %s", (user_id,), one=True)
            page = page[0]

        resp = self.read("SELECT LOWER(searchment) FROM user WHERE id = %s;", (user_id,), one=True)
        resp = resp[0]

        result = self.read("SELECT name FROM product WHERE LOWER(name) LIKE %s AND user_id IN (%s, %s) LIMIT %s OFFSET %s;", (f"%{resp.lower()}%", my_id, user_id, page_size, page_size*page))
        return result

    def search(self, user_id, resp) -> tuple:
        return self.read("SELECT name FROM product WHERE LOWER(name) LIKE %s AND user_id IN (%s, %s)", (f"%{resp.lower()}%", my_id, user_id))

    def user_exist(self, user_id) -> bool:
        return bool(self.read('SELECT id FROM user WHERE id = %s', (user_id,)))

    def new_user(self, user_id, username) -> None:
        self.do('INSERT INTO user(id, name) VALUES (%s, %s)', (user_id, username))


