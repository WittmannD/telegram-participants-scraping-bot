import json
import base64
from typing import Iterable, Sized

from telethon.sessions import SQLiteSession


class SQLiteCustomSession(SQLiteSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        custom_tables = [
            ('navigation_stack', """navigation_stack (
                user_id integer primary key,
                stack string
            )"""),
            ('scraping_settings', """scraping_settings (
                user_id integer primary key,
                number integer,
                link string
            )""")
        ]

        missing = []

        c = self._cursor()
        for tbl_name, tbl_definition in custom_tables:
            c.execute('select name from sqlite_master where type="table" and name=(?)', (tbl_name,))

            if c.fetchone():
                continue

            missing.append(tbl_definition)

        self._create_table(c, *missing)
        c.close()
        self.save()

    def get_settings(self, user_id: int):
        return self._execute('select number, link from scraping_settings where user_id = ?', user_id)

    def update_settings(self, user_id: int, settings: dict):
        row = self._execute('select number, link from scraping_settings where user_id = ?', user_id)
        old_number = None
        old_link = None
        if row:
            old_number, old_link = row

        number = settings.get('number', old_number)
        link = settings.get('link', old_link)
        self._execute('insert or replace into scraping_settings (user_id, number, link) values (?, ?, ?)',
                      user_id, number, link)

    def set_navigation_stack(self, user_id: int, navigation_stack: list[str]):
        if len(navigation_stack) > 100:
            navigation_stack = navigation_stack[len(navigation_stack) - 100:]
        encoded = str(base64.b64encode(json.dumps(navigation_stack[0:100]).encode('utf-8')), 'utf-8')
        self._execute('insert or replace into navigation_stack (user_id, stack) values (?, ?)', user_id, encoded)

    def get_navigation_stack(self, user_id: int):
        row = self._execute('select stack from navigation_stack where user_id = ?', user_id, )
        if row and row[0] != '':
            return json.loads(base64.b64decode(row[0]))
        else:
            return []
