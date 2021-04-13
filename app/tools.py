# -*- coding: utf-8 -*-


from sqlite3 import connect


class DataBase:
    def __init__(self, path='./database/files.db'):
        self.path: str = path

    def execute(self, command: str) -> str:
        with connect(self.path) as database:
            cur = database.cursor()
            result: str = cur.execute(command).fetchall()
        return result

    def get(self, value_key, page, value, one_result=True):
        result = self.execute(
            f'SELECT {value_key} FROM {page} WHERE name = "{value}"')
        if one_result:
            result = result[0][0]
        return result


class Files(DataBase):
    def __init__(self):
        super().__init__('./database/files.db')

    def get_file(self, name: str) -> str:
        return self.execute(
            f'SELECT path FROM files WHERE name = "{name}"')[0][0]


class Groups(DataBase):
    def __init__(self):
        super().__init__('./database/files.db')

    def get_groups(self, name: str) -> str:
        return self.execute(
            f'SELECT path FROM files WHERE name = "{name}"')[0][0]
