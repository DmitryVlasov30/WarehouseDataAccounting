from sqlite3 import connect
from loguru import logger
from config import settings


class Database:
    """
    База данных для хранения сокращений единиц измерения
    """
    def __init__(self, database_path, name_table):
        self.database_path = database_path
        self.connection = connect(database_path)
        self.cursor = self.connection.cursor()
        self.name_table = name_table

        self.create_table()

    def create_table(self):
        """
        создает таблицу, если не существует
        :return: None
        """
        self.cursor.execute(f"""
             CREATE TABLE IF NOT EXISTS {self.name_table} (
                "id"	INTEGER NOT NULL UNIQUE,  
                "full_unit_name"  TEXT NOT NULL,
                "short_unit_name"  TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

    def get_data(self):
        """
        возвращает все данные с бд
        :return: List[Tuple]
        """
        return self.cursor.execute(f"""SELECT * FROM {self.name_table}""").fetchall()

    def insert_data(self, full_unit, short_unit):
        """
        добавляет сокращение ед измерения в бд
        :param full_unit:  str
        :param short_unit: str
        :return: None
        """
        try:
            self.cursor.execute(f"""
                INSERT INTO {self.name_table} 
                (full_unit_name, short_unit_name) 
                VALUES (?, ?)
            """, (full_unit, short_unit))

            self.connection.commit()

            logger.info(f"добавлено сокращение {full_unit}, {short_unit}")
        except Exception as ex:
            self.connection.rollback()
            logger.error(f"Ошибка при добавлении данных: {ex}")
            raise ex

    def delete_data(self, full_name, short_name):
        """
        удаляет сокращение из бд
        :param full_name: str
        :param short_name: str
        :return: None
        """
        try:
            self.cursor.execute(f"""
                DELETE FROM {self.name_table}
                WHERE full_unit_name = ? AND short_unit_name = ?""", (full_name, short_name))
            logger.info(f"удалено сокращение {full_name}, {short_name}")
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            logger.error(ex)


class InvoicesDataBase:
    """
    База данных для хранения накладных
    """
    def __init__(self, database_path, name_table):
        self.database_path = database_path
        self.name_table = name_table

        self.connection = connect(database_path)
        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):
        """
        создание бд
        :return: None
        """
        self.cursor.execute(f"""
             CREATE TABLE IF NOT EXISTS {self.name_table} (
                "id"	INTEGER NOT NULL UNIQUE,
                "name" TEXT NOT NULL,
                "unit" TEXT NOT NULL,
                "count" INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

    def get_invoices(self):
        """
        получение данных из бд
        :return: List[Tuple]
        """
        return self.cursor.execute(f"""SELECT * FROM {self.name_table}""").fetchall()

    def insert_invoices(self, name, unit, count):
        """
        добавляет новый элемент из накладной
        :param name: str
        :param unit: str
        :param count: int | str
        :return: None
        """
        try:
            self.cursor.execute(f"""
                INSERT INTO {self.name_table} 
                (name, unit, count) 
                VALUES  (?, ?, ?)
            """, (name, unit, count))
            self.connection.commit()
            logger.info(f"Добавлен элемент {name}, {unit}, {count}")
        except Exception as ex:
            self.connection.rollback()
            logger.error(f"Ошибка при добавлении данных: {ex}")
            raise ex


if __name__ == '__main__':
    pass