import sqlite3

class Sqlite_db:
    def __init__(self, name_db, table_name, row_factory: bool = False):
        """
        :param name_db:
        :param row_factory: Если установить значение True, то к данным можно будет обращаться как к словарю(тип: <class 'sqlite3.Row'>, tuple(dat) - преобразрвывает в список,  dat.keys() - выдаёт все ключи и к данным можно обращаться так: dat['id'])
        """
        self.conn = sqlite3.connect(database=name_db)
        self.cur = self.conn.cursor()
        self.table_name = table_name
        if row_factory:
            self.cur.row_factory = sqlite3.Row

    def change_table_name(self, table_name) -> bool:
        """

        :param table_name: Имя, на которое меняете
        :return: Возвращает, существует ли таблица, если же нет, то нужно её создать, иначе выдаст ошибку
        """
        self.table_name = table_name
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if self.cur.fetchone() is None:
            return False
        else:
            return True

    def get_all_tables(self) -> list:
        if self.cur.row_factory is None:
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [name[0] for name in self.cur.fetchall()]
        else:
            self.cur.row_factory = None
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            self.cur.row_factory = sqlite3.Row
            return [name[0] for name in self.cur.fetchall()]

    def create_table(self, **kwargs):
        """NULL	Значение - значение NULL.\n
        INTEGER(INT)	Значение представляет собой целое число со знаком, сохраненное в 1, 2, 3, 4, 6 или 8 байтах в зависимости от величины значения.\n
        REAL	Значение представляет собой значение с плавающей запятой, которое хранится как 8-байтовое число с плавающей точкой IEEE.\n
        TEXT	Значение представляет собой текстовую строку, хранящуюся с использованием кодировки базы данных (UTF-8, UTF-16BE или UTF-16LE)\n
        BLOB	Значение представляет собой блок данных, который хранится точно так же, как он был введен."""
        exec = f'CREATE TABLE IF NOT EXISTS {self.table_name} '
        args = []
        if kwargs != {}:
            for key in kwargs.keys():
                args.append(f'{key} {kwargs[key]}')
            exec += f"({','.join(args)})"
        self.cur.execute(exec)

    def insert_data(self, **kwargs):
        exec = f'INSERT INTO {self.table_name} ({",".join(kwargs.keys())}) VALUES '
        args = []
        for key in kwargs.keys():
            if not str(kwargs[key]).isdigit():
                args.append(f"'{kwargs[key]}'")
            else: args.append(f'{kwargs[key]}')
        exec += f"({','.join(args)})"
        self.cur.execute(exec)
        self.conn.commit()

    def update_data(self, where: str = None, **kwargs):
        exec = f'UPDATE {self.table_name} SET '
        args = []
        for key in kwargs.keys():
            if not str(kwargs[key]).isdigit():
                args.append(f'{key} = "{kwargs[key]}" ')
            else:
                args.append(f'{key} = {kwargs[key]} ')
        exec += f"{','.join(args)}"
        if where is not None:
            exec += f'WHERE {where} '
        self.cur.execute(exec)
        self.conn.commit()

    def select_data(self, col_names='*', where: str = None, order_by: str = None, desc: bool = False) -> list:
        """
        :param table_name:  Название таблицы
        :param col_names:   Названия колонок, которые ищем(по умолчанию выбираются все)
        :param where:       Если нужно отсортировывать данные, то следует записывать так: where="price > 120", при условии, что price = int, со строкой: where="user_name = 'Имя'" | НЕ РАВНО <>
        :param order_by:    Сортировка выдаваемых данных, по определённым данным --- order_by="item_id"
        :param desc:        Сортировать в обратном порядке
        :return
        """
        exec = f'SELECT {col_names} FROM {self.table_name} '
        if where is not None:
            exec += f'WHERE {where} '
        if order_by is not None:
            exec += f'ORDER BY {order_by} '
        if desc:
            exec += 'DESC'
        data = self.cur.execute(exec)
        return data.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    db = Sqlite_db('test.db', row_factory=True, table_name='test_table')
    db.create_table(id='intenger', name='text', surname='blob')
