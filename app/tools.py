# -*- coding: utf-8 -*-


from sqlite3 import connect


class DataBase:
    def __init__(self, path):
        self.path: str = path

    def execute(self, command: str) -> str:
        with connect(self.path) as database:
            cur = database.cursor()
            result: str = cur.execute(command).fetchall()
        return result


class Pages(DataBase):
    def __init__(self):
        super().__init__('./database/files.db')

    def get_page(self, name: str) -> str:
        return self.execute(
            f'SELECT html FROM pages WHERE name = "{name}"')[0][0]


class Files(DataBase):
    def __init__(self):
        super().__init__('./database/files.db')

    def get_file(self, name: str) -> str:
        return self.execute(
            f'SELECT path FROM files WHERE name = "{name}"')[0][0]


