from sqlite3 import connect
from loguru import logger
from config import settings


class Database:
    def __init__(self, database_path, name_table):
        self.database_path = database_path
        self.connection = connect(database_path)
        self.cursor = self.connection.cursor()
        self.name_table = name_table

        self.create_table()

    def create_table(self):
        self.cursor.execute(f"""
             CREATE TABLE IF NOT EXISTS {self.name_table} (
                "id"	INTEGER NOT NULL UNIQUE,  
                "full_unit_name"  TEXT NOT NULL,
                "short_unit_name"  TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

    def get_data(self):
        return self.cursor.execute(f"""SELECT * FROM {self.name_table}""").fetchall()

    def insert_data(self, full_unit, short_unit):
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
    def __init__(self, database_path, name_table):
        self.database_path = database_path
        self.name_table = name_table

        self.connection = connect(database_path)
        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):
        self.cursor.execute(f"""
             CREATE TABLE IF NOT EXISTS {self.name_table} (
                "id"	INTEGER NOT NULL UNIQUE,
                "id_item" INTEGER NOT NULL UNIQUE,  
                "name" TEXT NOT NULL,
                "unit" TEXT NOT NULL,
                "count" INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

    def get_invoices(self):
        return self.cursor.execute(f"""SELECT * FROM {self.name_table}""").fetchall()

    def insert_invoices(self, id_item, name, unit, count):
        try:
            self.cursor.execute(f"""
                INSERT INTO {self.name_table} 
                (id_item, name, unit, count) 
                VALUES  (?, ?, ?, ?)
            """, (id_item, name, unit, count))
            self.connection.commit()
            logger.info(f"Добавлен элемент {id_item}, {name}, {unit}, {count}")
        except Exception as ex:
            self.connection.rollback()
            logger.error(f"Ошибка при добавлении данных: {ex}")
            raise ex

    def delete_invoices(self, id_item):
        try:
            self.cursor.execute(f"""
                DELETE FROM {self.name_table}
                WHERE id_item = ?""", (id_item,))
            logger.info(f"удалено сокращение {id_item}")
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            logger.error(ex)


if __name__ == '__main__':
    pass